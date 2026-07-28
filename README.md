# 隧道施工突涌水灾害韧性评估现场实施指南

[跳转到本文件英文版 / Jump to English](#english-version)

本仓库将论文 *Intelligent resilience assessment of water inrush in tunnel construction based on mixture of experts-LLMs system* 及其两个配套开源项目，转化为施工现场可执行、可复核、可留痕的实施指南。

它面向项目经理、总工程师、安全负责人、应急管理人员、造价人员和评估工程师，提供：

- 从事故资料采集到韧性等级判定的标准作业流程；
- 恢复时间与脆弱性评估表单；
- 证据、假设、缺失信息和置信度登记方法；
- 多名专家/LLM评估结果的 CI 加权与二维云模型计算工具；
- 韧性提升措施、责任人、期限和闭环验收表；
- 一套可重复运行的匿名演示案例。

> [!CAUTION]
> 本指南是工程决策支持工具，不替代应急预案、人员搜救、监测预警、停工撤人、专项施工方案、法定事故报告、设计复核或有资质单位的专业判断。事故发生后，人员生命安全和次生灾害控制始终优先。只有现场指挥机构确认具备评估条件后，才进入本指南的定量评估步骤。

## 现场最快用法

1. 打开 [`docs/quick-start.md`](docs/quick-start.md)，先执行安全门和15分钟初始登记。
2. 复制 [`templates/`](templates/) 下的表单到本次事件文件夹。
3. 按证据编号 `E01、E02...` 登记所有已知信息、来源、单位和状态。
4. 分别执行恢复时间和脆弱性工作流，不得由同一个结论反推输入。
5. 至少由两名相互独立的评估者完成评价；正式部署建议包含领域专家。
6. 运行：

   ```bash
   python tools/field_assessment.py examples/example-assessment.json --pretty
   ```

7. 由评估负责人复核自动校验结果、二维云模型等级和对应措施。
8. 将最终结果填入 [`templates/final-report.md`](templates/final-report.md)，经审批后发布。

## 实施流程

```mermaid
flowchart TD
    A["突涌水/突泥事件或演练"] --> B{"安全门是否满足？"}
    B -- 否 --> C["继续撤人、救援、封控和监测；暂不进行定量评估"]
    B -- 是 --> D["建立事件编号并登记证据、缺失项和版本"]
    D --> E["从知识图谱检索规则、相似案例和策略"]
    E --> F["恢复时间评估：A/B/C/D四阶段与关键路径"]
    E --> G["脆弱性评估：LP、LC、LE及去重"]
    F --> H["独立评估、区间表达和规则校验"]
    G --> H
    H --> I["CI加权样本与二维云模型"]
    I --> J["Level I-IV韧性判定"]
    J --> K["匹配措施、责任人、期限和验收证据"]
    K --> L["复评、关闭或升级"]
```

## 核心量化口径

恢复时间：

```text
Time = TA + TB + TC + TD
```

- `TA`：应急响应、人员撤离和风险消除；
- `TB`：排水、清淤、装运和合规处置；
- `TC`：供电、通风、排水系统及关键设备恢复；
- `TD`：地层加固、工法调整、验证、复工审批和施工组织恢复。

存在并行活动时，必须建立重叠台账并按关键路径计时，不能重复累计。

脆弱性：

```text
Loss = LP1 + LP2/3 + LP3/60
     + (LC1 + LC2 + LC3 + LC4)/400 + LE
```

其中：

- `LP1/LP2/LP3`：死亡、重伤、轻伤人数；
- `LC1`：排水清淤费用；
- `LC2`：设备损失；
- `LC3`：材料和已完工程损失；
- `LC4`：不与前三项重复的工期延误损失；
- `LC` 单位统一为万元人民币；
- `LE` 取 `0、0.5、1、3、10`。

维度分级边界如下：

| 维度等级 | 恢复时间 Time（月） | 脆弱性 Loss |
| --- | ---: | ---: |
| 1 | `[0, 0.33)` | `[0, 1)` |
| 2 | `[0.33, 1)` | `[1, 3)` |
| 3 | `[1, 3)` | `[3, 10)` |
| 4 | `[3, 9)` | `[10, 30)` |
| 5 | `[9, 24]` | `[30, 100]` |

物理恢复时间超过24个月时应保留原估计，同时将云模型输入截断为24个月并明确标记。`Loss > 100` 时不得静默截断，应标记为超出参考域并按项目批准规则处理。

## 仓库内容

| 路径 | 用途 |
| --- | --- |
| [`docs/field-implementation-guide.md`](docs/field-implementation-guide.md) | 完整现场实施手册 |
| [`docs/quick-start.md`](docs/quick-start.md) | 事故后快速启动卡 |
| [`docs/deployment.md`](docs/deployment.md) | 项目部署、知识图谱和离线准备 |
| [`docs/training-and-drills.md`](docs/training-and-drills.md) | 培训、桌面推演和验收要求 |
| [`templates/`](templates/) | 可复制的登记表、台账和报告模板 |
| [`examples/`](examples/) | 匿名演示案例及计算输入 |
| [`tools/field_assessment.py`](tools/field_assessment.py) | 区间、分级、CI加权和二维云模型工具 |
| [`tests/`](tests/) | 计算规则的自动化测试 |

## 与另外两个开源项目的关系

- [tunnel-water-mud-inrush-resilience-kg](https://github.com/Huaiyuan-Sun/tunnel-water-mud-inrush-resilience-kg)：提供指标、规则、案例、等级和策略的知识图谱。
- [tunnel-resilience-assessment-workflows](https://github.com/Huaiyuan-Sun/tunnel-resilience-assessment-workflows)：提供恢复时间和脆弱性的结构化评估工作流。
- 本仓库：规定现场由谁、在何时、使用哪些表单、按什么门槛执行上述方法，并把结果转化为责任明确的行动闭环。

## 结果状态

每次评估必须使用以下状态之一：

- `Assessable`：关键输入足以形成可复核的点值或区间；
- `Provisional`：可形成有工程边界的临时结果，但关键资料仍待补充；
- `Not assessable`：无法为主导项建立合理边界；
- `Suspended`：安全条件、数据完整性或审批条件不允许继续。

任何 `Not assessable` 或未关闭的强制校验失败，都不得被包装成正式韧性等级。

## 现场运行包

建议每个项目在开工前建立一个可离线使用的“韧性评估运行包”，至少包括：

- 已批准的岗位与CI名册；
- 设备、泵排、运输、备件、供应商和外援能力清单；
- 项目单价、净延误费率及经济损失归类规则；
- 环境敏感受体、外排路径和许可条件；
- 本仓库表单、计算脚本、测试结果和固定发布版本；
- 两套演练情景及复盘记录；
- 原始证据只读区、工作区、审批区和归档区。

现场启动顺序固定为“安全—事实—区间—独立评估—校验—融合—行动—复评”。任何自动化输出必须保留人工审批，不得直接触发复工、撤人、救援或对外发布。

## 版本与引用

当前版本：`v1.1.0`

引用信息见 [`CITATION.cff`](CITATION.cff)。本仓库采用 [MIT License](LICENSE)。

---

<a id="english-version"></a>

# Field Implementation Guide for Tunnel Water-Inrush Resilience Assessment

This repository translates the paper *Intelligent resilience assessment of water inrush in tunnel construction based on mixture of experts-LLMs system* and its two companion repositories into a field-ready, reviewable, and traceable operating system.

It is intended for project managers, chief engineers, safety and emergency teams, cost engineers, environmental personnel, and assessment engineers. The package provides:

- a safety-gated procedure from incident intake to resilience classification;
- recovery-time and vulnerability assessment forms;
- evidence, assumption, missing-data, and confidence controls;
- confidence-index (CI) weighting and a reproducible two-dimensional cloud-model calculator;
- action ownership, deadlines, acceptance evidence, reassessment, and closure;
- an anonymized worked example and automated tests.

> [!CAUTION]
> This repository supports engineering decisions. It does not replace an emergency response plan, evacuation, rescue, monitoring, stop-work authority, statutory reporting, design verification, restart approval, or qualified professional judgment. Life safety and secondary-hazard control always take priority.

## Fastest field use

1. Open [`docs/quick-start.md`](docs/quick-start.md) and complete the safety gate.
2. Copy the forms in [`templates/`](templates/) into a new incident folder.
3. Assign `E01`, `E02`, and subsequent identifiers to every evidence item.
4. Record each input as `Observed`, `Derived`, `Assumed`, or `Unknown`.
5. Complete recovery-time and vulnerability assessments independently.
6. Obtain at least two independent evaluator results using the same evidence snapshot.
7. Run:

   ```bash
   python tools/field_assessment.py examples/example-assessment.json --pretty
   ```

8. Review warnings, boundary crossings, feature-point distances, and the proposed Level I-IV result.
9. Approve actions in [`templates/final-report.md`](templates/final-report.md), assign owners, and define reassessment triggers.

## Method summary

Recovery time is:

```text
Time = TA + TB + TC + TD
```

where A covers emergency response and risk control, B covers drainage and mud/debris removal, C covers equipment and system recovery, and D covers restoration of construction conditions and restart approval. Parallel work must be handled through a dependency and overlap ledger.

Vulnerability is:

```text
Loss = LP1 + LP2/3 + LP3/60
     + (LC1 + LC2 + LC3 + LC4)/400 + LE
```

`LP1`, `LP2`, and `LP3` are fatalities, serious injuries, and minor injuries. `LC1`-`LC4` are mutually exclusive direct-loss categories in CNY 10,000. Environmental level is mapped to `LE = 0, 0.5, 1, 3, or 10`.

| Dimension level | Time (months) | Loss |
| --- | ---: | ---: |
| 1 | `[0, 0.33)` | `[0, 1)` |
| 2 | `[0.33, 1)` | `[1, 3)` |
| 3 | `[1, 3)` | `[3, 10)` |
| 4 | `[3, 9)` | `[10, 30)` |
| 5 | `[9, 24]` | `[30, 100]` |

Physical estimates outside the reference domain must be retained and explicitly flagged. They must not be silently forced into the model domain.

## Repository map

| Path | Purpose |
| --- | --- |
| [`docs/field-implementation-guide.md`](docs/field-implementation-guide.md) | Complete field implementation manual |
| [`docs/quick-start.md`](docs/quick-start.md) | First 15 minutes, first hour, and first-day action card |
| [`docs/deployment.md`](docs/deployment.md) | Project deployment, knowledge graph, offline mode, and governance |
| [`docs/training-and-drills.md`](docs/training-and-drills.md) | Training, exercises, competency, and acceptance |
| [`templates/`](templates/) | Bilingual operational forms and audit records |
| [`examples/`](examples/) | An anonymized end-to-end example |
| [`tools/field_assessment.py`](tools/field_assessment.py) | Validation, interval, CI, and cloud-model calculator |
| [`tests/`](tests/) | Automated rule tests |

## Required result states

- `Assessable`: key inputs support a reviewable point or interval result.
- `Provisional`: a bounded interim result is possible, but material evidence remains outstanding.
- `Not assessable`: no defensible bound can be established for a controlling component.
- `Suspended`: safety, data integrity, or authorization conditions prohibit continuation.

An unresolved mandatory validation failure or `Not assessable` controlling component must never be presented as a formal resilience level.

## Field operating package

Before high-risk work starts, prepare an offline package containing the approved role and CI register, resource and supplier capacities, loss-accounting rules, environmental receptors and discharge constraints, this repository release, completed calculator tests, drill scenarios, and a controlled evidence/archive structure.

The fixed operating sequence is **safety → facts → intervals → independent assessments → validation → fusion → actions → reassessment**. Automated results always require human approval.

## Version and citation

Current version: `v1.1.0`

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). The repository is released under the [MIT License](LICENSE).
