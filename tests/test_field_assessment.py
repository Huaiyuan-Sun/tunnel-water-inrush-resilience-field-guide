import importlib.util
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "field_assessment.py"
SPEC = importlib.util.spec_from_file_location("field_assessment", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class FieldAssessmentTests(unittest.TestCase):
    def test_dimension_boundaries(self):
        self.assertEqual(MODULE.classify(0.0, MODULE.TIME_INTERVALS), 1)
        self.assertEqual(MODULE.classify(0.33, MODULE.TIME_INTERVALS), 2)
        self.assertEqual(MODULE.classify(1.0, MODULE.TIME_INTERVALS), 3)
        self.assertEqual(MODULE.classify(24.0, MODULE.TIME_INTERVALS), 5)
        self.assertIsNone(MODULE.classify(24.1, MODULE.TIME_INTERVALS))

    def test_resilience_cell_counts(self):
        counts = {"I": 0, "II": 0, "III": 0, "IV": 0}
        for point in MODULE.feature_points():
            counts[point["resilience_level"]] += 1
        self.assertEqual(counts, {"I": 3, "II": 7, "III": 9, "IV": 6})

    def test_example_is_valid_and_reproducible(self):
        payload = json.loads(
            (ROOT / "examples" / "example-assessment.json").read_text(encoding="utf-8")
        )
        first = MODULE.assess(payload)
        second = MODULE.assess(payload)
        self.assertEqual(first["validation"]["status"], "PASS_WITH_WARNINGS")
        self.assertEqual(first["cloud_model"]["resilience_level"], "II")
        self.assertEqual(
            first["cloud_model"]["resilience_level"],
            second["cloud_model"]["resilience_level"],
        )
        self.assertAlmostEqual(
            first["cloud_model"]["nearest_feature_point"]["average_distance"],
            second["cloud_model"]["nearest_feature_point"]["average_distance"],
        )

    def test_casualty_upper_bound_is_enforced(self):
        bad = {
            "affected_workers": 2,
            "LP1": [1, 1],
            "LP2": [1, 1],
            "LP3": [1, 1],
            "LC1": [0, 0],
            "LC2": [0, 0],
            "LC3": [0, 0],
            "LC4": [0, 0],
            "environmental_levels": [1, 1],
        }
        with self.assertRaises(MODULE.AssessmentInputError):
            MODULE.assess_vulnerability(bad)


if __name__ == "__main__":
    unittest.main()
