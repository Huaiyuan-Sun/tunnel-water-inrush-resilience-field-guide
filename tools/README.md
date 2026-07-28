# 计算工具

`field_assessment.py` 仅使用 Python 标准库，支持：

- A—D净阶段区间加和；
- 24个月模型输入截断与警告；
- LP人员上限和整数校验；
- LC与LE的Loss区间计算；
- Time/Loss等级和跨级识别；
- CI整数权重；
- 二维逆向/正向云发生器；
- 25个韧性特征点平均距离和Level I—IV判定；
- 固定随机种子的可重复输出。

运行：

```bash
python tools/field_assessment.py examples/example-assessment.json --pretty
```

保存结果：

```bash
python tools/field_assessment.py examples/example-assessment.json \
  --pretty --output output/example-result.json
```

运行测试：

```bash
python -m unittest discover -s tests -v
```

## 输入约定

- 所有区间均为 `[lower, upper]`；
- A—D为去除重叠后的净阶段时长，单位为月；
- LP为人数且边界必须是整数；
- LC单位为万元人民币；
- 环境等级为1—5，工具自动映射LE；
- 每名评估者提供用于云模型的 `time`、`loss` 和正整数 `ci`；
- 超过模型域的评估值不得直接输入，应先按指南处理并保留物理估计。

## 复现记录

正式报告应保存：

- 输入JSON；
- 输出JSON；
- 仓库提交号；
- Python版本；
- 随机种子；
- 云滴数；
- 执行命令；
- 人工复核和审批记录。

## 输出解释

- `validation.status` 只说明机器校验状态，不等于允许复工；
- `dimension_level_range` 表示物理区间跨越的单维等级；
- `resilience_level` 是云模型建议的综合Level I—IV；
- `nearest_feature_point` 与第二近点距离差较小时，应标记边界敏感；
- 警告必须进入最终报告，不得只保留在终端窗口。

---

<a id="english-version"></a>

# Calculator

`field_assessment.py` uses only the Python standard library. It supports net Stage A-D interval addition, 24-month model-input handling, integer and casualty-limit validation, Loss calculation, Time/Loss dimension levels, positive-integer CI weights, backward/forward two-dimensional cloud generation, and mean distance to all 25 Level I-IV feature points.

Run:

```bash
python tools/field_assessment.py examples/example-assessment.json --pretty
```

Save output:

```bash
python tools/field_assessment.py examples/example-assessment.json \
  --pretty --output output/example-result.json
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Input contract

- Every interval is `[lower, upper]`.
- A-D are net stage durations after overlap treatment, in months.
- LP values are persons and must have integer bounds.
- LC values use CNY 10,000.
- Environmental level is 1-5 and is mapped to LE by the tool.
- Every evaluator supplies `time`, `loss`, and positive-integer `ci`.
- Out-of-domain physical estimates must be handled under the guide and retained.

## Reproducibility record

Retain the input and output JSON, repository commit, Python version, seed, droplet count, command, and human review/approval.

## Output interpretation

`validation.status` is a machine-validation state, not restart authorization. `dimension_level_range` describes a physical interval across dimension levels, whereas `resilience_level` is the proposed integrated Level I-IV. A small margin between the nearest and second-nearest feature points requires boundary-sensitivity review. Copy every warning into the report.
