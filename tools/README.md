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

