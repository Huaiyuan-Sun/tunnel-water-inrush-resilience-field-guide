# 匿名演示案例

> 本案例仅用于演示表单、校验和计算流程，不对应论文中的四个工程案例，也不得作为任何实际项目的默认参数。

## 1. 情景

某山岭隧道掌子面发生持续涌水并夹带少量泥砂。班组12人已全部确认，现场无死亡，轻伤已确认1人，另有1名人员伤情等级待复核。有效排水能力大于持续流量，但积水量、设备拆检结果、环境外排范围和注浆验证周期仍存在不确定性。

证据示例见 [`example-evidence.csv`](example-evidence.csv)。

## 2. 恢复时间

去除重叠后的阶段区间：

| 阶段 | 区间（月） | 主要依据 |
| --- | ---: | --- |
| A | 0.08—0.12 | 撤离、封控和准入 |
| B | 0.55—0.75 | 净排水能力、积水量、清淤运输 |
| C | 0.40—0.60 | 电气和设备拆检、维修 |
| D | 1.50—1.80 | 注浆、监测验证和复工审批 |

因此：

```text
Time = [2.53, 3.27] months
representative = 2.90 months
level_range = [3, 4]
```

区间跨越3个月边界，因此置信度不能为 `High`。D阶段为主导项，应优先补充注浆范围、验证轮次和复工审批时长。

## 3. 脆弱性

输入区间：

```text
LP1=[0,0], LP2=[0,1], LP3=[1,3]
LC1=[80,120], LC2=[40,80], LC3=[20,50], LC4=[120,200]
Environmental level=[2,3], LE=[0.5,1]
```

计算：

```text
Loss_low  = 0 + 0/3 + 1/60 + (80+40+20+120)/400 + 0.5
          = 1.1667

Loss_high = 0 + 1/3 + 3/60 + (120+80+50+200)/400 + 1
          = 2.5083

representative = 1.8375
level_range = [2,2]
```

## 4. 独立评估与CI

| 评估者 | Time | Loss | CI |
| --- | ---: | ---: | ---: |
| ENG-01 | 2.4 | 1.8 | 3 |
| LLM-01 | 2.8 | 2.1 | 2 |
| LLM-02 | 3.1 | 2.4 | 1 |

这些单值是各评估者已完成规则校验后的代表值。区间仍保存在各自评估记录中。

## 5. 运行

```bash
python tools/field_assessment.py examples/example-assessment.json --pretty
```

预期：

- 工具识别恢复时间区间跨级；
- LP上界不超过12人；
- Loss算术可复现；
- 使用固定种子生成相同的云模型结果；
- 输出最近和次近特征点、距离差与Level I—IV等级。

在 `v1.0.0`、5000个云滴和随机种子42下，计算得到：

```text
Ex=2.6500, Ey=2.0000
Enx=0.3133, Eny=0.2507
Hex=0.1057, Hey=0.0532
nearest feature point = DII-T3-L2
average distance = 0.9112
resilience level = Level II
```

随机种子或云滴数改变时，平均距离可有轻微变化，因此正式报告必须同时记录两者。

## 6. 行动

该案例的主导不确定性和恢复瓶颈是D阶段。行动计划不应只依据综合等级，还应至少包括：

1. 在规定时间内完成注浆范围和轮次确认；
2. 明确监测稳定判据和复工审批资料；
3. 更新设备拆检清单，缩小C阶段区间；
4. 核实排放路径和受体，关闭环境等级区间；
5. 新证据到达后创建 `EVID-v4` 并重新运行评估。

## 7. 审计与复评要点

- `EVID-v3`必须冻结后再发给三名评估者；
- 评估者不得先看到他人代表值；
- 所有区间、假设和CI依据随输入JSON一并归档；
- 3个月边界、D阶段和环境等级区间列入复评优先项；
- 注浆验证周期、设备拆检和受体核实任一更新后，创建新版本并比较等级、区间宽度及最近点距离变化。

---

<a id="english-version"></a>

# Anonymized Worked Example

> This example demonstrates forms, validations, and calculations only. It is not one of the four cases in the paper and must not become a default parameter set for a real project.

## 1. Scenario

A mountain tunnel face experiences continuing water inflow with limited sediment. All 12 workers are accounted for. There are no confirmed fatalities; one minor injury is confirmed and one injury classification remains under review. Effective drainage capacity exceeds continuing inflow, but accumulated volume, equipment inspection, environmental discharge extent, and grouting-verification duration remain uncertain.

See [`example-evidence.csv`](example-evidence.csv).

## 2. Recovery time

Net stage intervals after overlap treatment are:

| Stage | Interval (months) | Main basis |
| --- | ---: | --- |
| A | 0.08-0.12 | Evacuation, access control, and safe entry |
| B | 0.55-0.75 | Net drainage, accumulated water, mud and transport |
| C | 0.40-0.60 | Electrical/equipment inspection and repair |
| D | 1.50-1.80 | Grouting, monitoring verification, and restart approval |

```text
Time = [2.53, 3.27] months
representative = 2.90 months
level_range = [3, 4]
```

The interval crosses the three-month boundary, so confidence cannot be `High`. Stage D controls the result; evidence collection should prioritize grouting extent, verification rounds, and approval duration.

## 3. Vulnerability

```text
LP1=[0,0], LP2=[0,1], LP3=[1,3]
LC1=[80,120], LC2=[40,80], LC3=[20,50], LC4=[120,200]
Environmental level=[2,3], LE=[0.5,1]
```

```text
Loss_low  = 0 + 0/3 + 1/60 + (80+40+20+120)/400 + 0.5
          = 1.1667

Loss_high = 0 + 1/3 + 3/60 + (120+80+50+200)/400 + 1
          = 2.5083

representative = 1.8375
level_range = [2,2]
```

## 4. Independent evaluators and CI

| Evaluator | Time | Loss | CI |
| --- | ---: | ---: | ---: |
| ENG-01 | 2.4 | 1.8 | 3 |
| LLM-01 | 2.8 | 2.1 | 2 |
| LLM-02 | 3.1 | 2.4 | 1 |

The representative values are supplied only after each evaluator completes the same rule validation. Their original intervals remain in the assessment record.

## 5. Run and expected result

```bash
python tools/field_assessment.py examples/example-assessment.json --pretty
```

For version `v1.1.0`, 5,000 droplets, and seed 42:

```text
Ex=2.6500, Ey=2.0000
Enx=0.3133, Eny=0.2507
Hex=0.1057, Hey=0.0532
nearest feature point = DII-T3-L2
average distance = 0.9112
resilience level = Level II
```

The tool also reports the cross-level recovery interval, casualty upper-bound validation, reproducible Loss arithmetic, all feature-point distances, and the second-nearest point. Record the seed and droplet count because changing them may slightly change mean distances.

## 6. Actions

Stage D is the controlling recovery bottleneck. The plan should:

1. confirm the grouting scope and number of rounds;
2. define monitoring stability and restart-approval evidence;
3. update the equipment inspection list to narrow Stage C;
4. verify the discharge pathway and receptor to close the environmental interval;
5. create `EVID-v4` and rerun the assessment when new evidence arrives.

## 7. Audit and reassessment

Freeze `EVID-v3` before distribution. Evaluators do not see each other's outputs. Archive every interval, assumption, CI basis, input, and output. Reassess after any grouting-verification, equipment-inspection, or receptor update, comparing the level, interval width, and nearest-point margin with the prior version.
