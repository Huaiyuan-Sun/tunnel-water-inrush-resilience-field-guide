#!/usr/bin/env python3
"""Field calculator for tunnel water-inrush resilience assessment.

The script uses only the Python standard library. It validates the structured
input, calculates recovery-time and vulnerability intervals, builds a
confidence-index-weighted two-dimensional cloud, and finds the nearest of the
25 resilience feature points described by the accompanying field guide.

It is a decision-support implementation, not an emergency command system.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Iterable


TIME_INTERVALS = (
    (0.0, 0.33),
    (0.33, 1.0),
    (1.0, 3.0),
    (3.0, 9.0),
    (9.0, 24.0),
)
LOSS_INTERVALS = (
    (0.0, 1.0),
    (1.0, 3.0),
    (3.0, 10.0),
    (10.0, 30.0),
    (30.0, 100.0),
)
ENVIRONMENTAL_EQUIVALENTS = {1: 0.0, 2: 0.5, 3: 1.0, 4: 3.0, 5: 10.0}
STAGES = ("A", "B", "C", "D")
LP_COMPONENTS = ("LP1", "LP2", "LP3")
LC_COMPONENTS = ("LC1", "LC2", "LC3", "LC4")
EPSILON = 1e-12


class AssessmentInputError(ValueError):
    """Raised when an input violates a mandatory assessment rule."""


def interval(value: Any, name: str, *, integers: bool = False) -> tuple[float, float]:
    if not isinstance(value, list) or len(value) != 2:
        raise AssessmentInputError(f"{name} must be [lower, upper].")
    try:
        low, high = float(value[0]), float(value[1])
    except (TypeError, ValueError) as exc:
        raise AssessmentInputError(f"{name} contains a non-numeric value.") from exc
    if not (math.isfinite(low) and math.isfinite(high)):
        raise AssessmentInputError(f"{name} must contain finite values.")
    if low < 0 or high < 0:
        raise AssessmentInputError(f"{name} cannot be negative.")
    if low > high:
        raise AssessmentInputError(f"{name} lower bound exceeds upper bound.")
    if integers and (not low.is_integer() or not high.is_integer()):
        raise AssessmentInputError(f"{name} bounds must be integers.")
    return low, high


def midpoint(bounds: tuple[float, float]) -> float:
    return (bounds[0] + bounds[1]) / 2.0


def classify(value: float, ranges: tuple[tuple[float, float], ...]) -> int | None:
    for index, (low, high) in enumerate(ranges, start=1):
        if index < len(ranges) and low <= value < high:
            return index
        if index == len(ranges) and low <= value <= high:
            return index
    return None


def dimension_level_range(
    bounds: tuple[float, float], ranges: tuple[tuple[float, float], ...]
) -> list[int | None]:
    return [classify(bounds[0], ranges), classify(bounds[1], ranges)]


def resilience_level(time_level: int, loss_level: int) -> str:
    level_sum = time_level + loss_level
    if 2 <= level_sum <= 3:
        return "I"
    if 4 <= level_sum <= 5:
        return "II"
    if 6 <= level_sum <= 7:
        return "III"
    if 8 <= level_sum <= 10:
        return "IV"
    raise AssessmentInputError("Dimension levels must each be between 1 and 5.")


def assess_recovery(data: dict[str, Any]) -> dict[str, Any]:
    stages = data.get("stages")
    if not isinstance(stages, dict) or set(stages) != set(STAGES):
        raise AssessmentInputError("recovery.stages must contain exactly A, B, C, and D.")

    parsed = {stage: interval(stages[stage], f"recovery.stages.{stage}") for stage in STAGES}
    physical = (
        sum(parsed[stage][0] for stage in STAGES),
        sum(parsed[stage][1] for stage in STAGES),
    )
    representative = midpoint(physical)
    model_bounds = (min(physical[0], 24.0), min(physical[1], 24.0))
    model_representative = min(representative, 24.0)
    level_bounds = dimension_level_range(model_bounds, TIME_INTERVALS)
    representative_level = classify(model_representative, TIME_INTERVALS)
    warnings: list[str] = []
    if physical[1] > 24.0:
        warnings.append(
            "Physical recovery estimate exceeds 24 months; cloud-model input was truncated."
        )
    if level_bounds[0] != level_bounds[1]:
        warnings.append("Recovery interval crosses at least one level boundary.")

    return {
        "stage_intervals_months": {key: list(value) for key, value in parsed.items()},
        "time_interval_months_physical": list(physical),
        "time_representative_months_physical": representative,
        "time_interval_months_model_input": list(model_bounds),
        "time_representative_months_model_input": model_representative,
        "time_level": representative_level,
        "time_level_range": level_bounds,
        "upper_bound_truncated": physical[1] > 24.0,
        "warnings": warnings,
    }


def assess_vulnerability(data: dict[str, Any]) -> dict[str, Any]:
    affected_workers = data.get("affected_workers")
    if affected_workers is None:
        raise AssessmentInputError("vulnerability.affected_workers is required.")
    affected = interval(
        affected_workers if isinstance(affected_workers, list) else [affected_workers] * 2,
        "vulnerability.affected_workers",
        integers=True,
    )

    lp = {
        name: interval(data.get(name), f"vulnerability.{name}", integers=True)
        for name in LP_COMPONENTS
    }
    lc = {name: interval(data.get(name), f"vulnerability.{name}") for name in LC_COMPONENTS}

    casualty_low = sum(lp[name][0] for name in LP_COMPONENTS)
    casualty_high = sum(lp[name][1] for name in LP_COMPONENTS)
    if casualty_low > affected[0]:
        raise AssessmentInputError(
            "Lower casualty scenario exceeds the lower affected-worker scenario."
        )
    if casualty_high > affected[1]:
        raise AssessmentInputError(
            "Upper casualty scenario exceeds the upper affected-worker scenario."
        )

    env_levels = interval(
        data.get("environmental_levels"),
        "vulnerability.environmental_levels",
        integers=True,
    )
    env_low_level, env_high_level = int(env_levels[0]), int(env_levels[1])
    if env_low_level not in ENVIRONMENTAL_EQUIVALENTS or env_high_level not in ENVIRONMENTAL_EQUIVALENTS:
        raise AssessmentInputError("Environmental levels must be integers from 1 to 5.")
    le = (
        ENVIRONMENTAL_EQUIVALENTS[env_low_level],
        ENVIRONMENTAL_EQUIVALENTS[env_high_level],
    )

    loss_low = (
        lp["LP1"][0]
        + lp["LP2"][0] / 3.0
        + lp["LP3"][0] / 60.0
        + sum(lc[name][0] for name in LC_COMPONENTS) / 400.0
        + le[0]
    )
    loss_high = (
        lp["LP1"][1]
        + lp["LP2"][1] / 3.0
        + lp["LP3"][1] / 60.0
        + sum(lc[name][1] for name in LC_COMPONENTS) / 400.0
        + le[1]
    )
    loss_bounds = (loss_low, loss_high)
    representative = midpoint(loss_bounds)
    representative_level = classify(representative, LOSS_INTERVALS)
    level_bounds = dimension_level_range(loss_bounds, LOSS_INTERVALS)
    warnings: list[str] = []
    if loss_high > 100.0:
        warnings.append("Loss exceeds the reference domain; it was not silently capped.")
    if level_bounds[0] != level_bounds[1]:
        warnings.append("Vulnerability interval crosses at least one level boundary.")

    return {
        "affected_workers": list(affected),
        "LP_persons": {key: list(value) for key, value in lp.items()},
        "LC_10000_RMB": {key: list(value) for key, value in lc.items()},
        "environmental_level": [env_low_level, env_high_level],
        "LE": list(le),
        "loss_interval": list(loss_bounds),
        "loss_representative": representative,
        "vulnerability_level": representative_level,
        "vulnerability_level_range": level_bounds,
        "outside_reference_domain": loss_high > 100.0,
        "warnings": warnings,
    }


def weighted_cloud_parameters(
    samples: list[tuple[float, float, int]]
) -> dict[str, float]:
    total_weight = sum(weight for _, _, weight in samples)
    if total_weight < 2:
        raise AssessmentInputError("Total CI weight must be at least 2 for sample variance.")

    ex = sum(x * weight for x, _, weight in samples) / total_weight
    ey = sum(y * weight for _, y, weight in samples) / total_weight
    sx2 = sum(weight * (x - ex) ** 2 for x, _, weight in samples) / (total_weight - 1)
    sy2 = sum(weight * (y - ey) ** 2 for _, y, weight in samples) / (total_weight - 1)
    enx = math.sqrt(math.pi / 2.0) * (
        sum(weight * abs(x - ex) for x, _, weight in samples) / total_weight
    )
    eny = math.sqrt(math.pi / 2.0) * (
        sum(weight * abs(y - ey) for _, y, weight in samples) / total_weight
    )
    hex_ = math.sqrt(abs(sx2 - enx**2))
    hey = math.sqrt(abs(sy2 - eny**2))
    return {
        "Ex": ex,
        "Ey": ey,
        "Enx": enx,
        "Eny": eny,
        "Hex": hex_,
        "Hey": hey,
    }


def feature_points() -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []
    for time_level, (time_low, time_high) in enumerate(TIME_INTERVALS, start=1):
        for loss_level, (loss_low, loss_high) in enumerate(LOSS_INTERVALS, start=1):
            points.append(
                {
                    "id": f"D{resilience_level(time_level, loss_level)}-T{time_level}-L{loss_level}",
                    "resilience_level": resilience_level(time_level, loss_level),
                    "time_level": time_level,
                    "loss_level": loss_level,
                    "x": (time_low + time_high) / 2.0,
                    "y": (loss_low + loss_high) / 2.0,
                    "z": 1.0,
                }
            )
    return points


def cloud_assessment(
    evaluators: Any, cloud_config: dict[str, Any] | None = None
) -> dict[str, Any]:
    if not isinstance(evaluators, list) or len(evaluators) < 2:
        raise AssessmentInputError("At least two independent evaluator records are required.")

    records: list[dict[str, Any]] = []
    samples: list[tuple[float, float, int]] = []
    for index, item in enumerate(evaluators):
        if not isinstance(item, dict):
            raise AssessmentInputError(f"evaluators[{index}] must be an object.")
        evaluator_id = str(item.get("id", "")).strip()
        if not evaluator_id:
            raise AssessmentInputError(f"evaluators[{index}].id is required.")
        try:
            time = float(item["time"])
            loss = float(item["loss"])
            ci_raw = float(item["ci"])
        except (KeyError, TypeError, ValueError) as exc:
            raise AssessmentInputError(
                f"evaluators[{index}] requires numeric time, loss, and ci."
            ) from exc
        if not all(math.isfinite(value) for value in (time, loss, ci_raw)):
            raise AssessmentInputError(f"evaluators[{index}] contains a non-finite value.")
        if time < 0 or time > 24:
            raise AssessmentInputError(
                f"evaluators[{index}].time must be within the model domain [0, 24]."
            )
        if loss < 0 or loss > 100:
            raise AssessmentInputError(
                f"evaluators[{index}].loss must be within the reference domain [0, 100]."
            )
        if not ci_raw.is_integer() or ci_raw <= 0:
            raise AssessmentInputError(f"evaluators[{index}].ci must be a positive integer.")
        ci = int(ci_raw)
        records.append({"id": evaluator_id, "time": time, "loss": loss, "ci": ci})
        samples.append((time, loss, ci))

    config = cloud_config or {}
    droplets = int(config.get("droplets", 5000))
    seed = int(config.get("seed", 42))
    if droplets < 100:
        raise AssessmentInputError("cloud.droplets must be at least 100.")

    params = weighted_cloud_parameters(samples)
    rng = random.Random(seed)
    points = feature_points()
    distance_sums = {point["id"]: 0.0 for point in points}
    outside_count = 0

    for _ in range(droplets):
        enny_x = rng.gauss(params["Enx"], params["Hex"])
        enny_y = rng.gauss(params["Eny"], params["Hey"])
        sigma_x = max(abs(enny_x), EPSILON)
        sigma_y = max(abs(enny_y), EPSILON)
        x = rng.gauss(params["Ex"], sigma_x)
        y = rng.gauss(params["Ey"], sigma_y)
        exponent = -(
            ((x - params["Ex"]) ** 2) / (2.0 * sigma_x**2)
            + ((y - params["Ey"]) ** 2) / (2.0 * sigma_y**2)
        )
        membership = math.exp(exponent)
        if not (0.0 <= x <= 24.0 and 0.0 <= y <= 100.0):
            outside_count += 1
        for point in points:
            distance_sums[point["id"]] += math.sqrt(
                (x - point["x"]) ** 2
                + (y - point["y"]) ** 2
                + (membership - point["z"]) ** 2
            )

    point_index = {point["id"]: point for point in points}
    distances = [
        {
            **point_index[point_id],
            "average_distance": distance_sum / droplets,
        }
        for point_id, distance_sum in distance_sums.items()
    ]
    distances.sort(key=lambda item: item["average_distance"])
    nearest, second = distances[0], distances[1]
    return {
        "evaluators": records,
        "total_ci_weight": sum(record["ci"] for record in records),
        "cloud_parameters": params,
        "droplets": droplets,
        "seed": seed,
        "outside_reference_fraction": outside_count / droplets,
        "nearest_feature_point": nearest,
        "second_nearest_feature_point": second,
        "nearest_distance_margin": second["average_distance"] - nearest["average_distance"],
        "resilience_level": nearest["resilience_level"],
        "feature_point_distances": distances,
    }


def assess(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise AssessmentInputError("Input root must be a JSON object.")
    result: dict[str, Any] = {
        "schema_version": "1.0",
        "incident_id": payload.get("incident_id"),
        "evidence_version": payload.get("evidence_version"),
    }
    recovery = assess_recovery(payload.get("recovery", {}))
    vulnerability = assess_vulnerability(payload.get("vulnerability", {}))
    result["recovery"] = recovery
    result["vulnerability"] = vulnerability

    evaluators = payload.get("evaluators")
    if evaluators is not None:
        result["cloud_model"] = cloud_assessment(evaluators, payload.get("cloud"))
    else:
        result["cloud_model"] = None

    warnings = [*recovery["warnings"], *vulnerability["warnings"]]
    if result["cloud_model"] and result["cloud_model"]["outside_reference_fraction"] > 0.05:
        warnings.append("More than 5% of simulated cloud droplets are outside the reference domain.")
    result["validation"] = {
        "status": "PASS" if not warnings else "PASS_WITH_WARNINGS",
        "warnings": warnings,
    }
    return result


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Assessment JSON file")
    parser.add_argument("--output", type=Path, help="Optional output JSON file")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = assess(payload)
    except (OSError, json.JSONDecodeError, AssessmentInputError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    text = json.dumps(
        result,
        ensure_ascii=False,
        indent=2 if args.pretty else None,
        sort_keys=args.pretty,
    )
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

