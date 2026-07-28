# 项目部署指南

## 1. 推荐部署形态

### 最低可用配置

- 一台可运行 Python 3.9+ 的离线电脑；
- 本仓库的只读发布版本；
- 现场表单的本地副本；
- 已批准的 CI 名册；
- 项目设备、单价、外援和审批时长清单。

### 标准配置

- Neo4j 知识图谱；
- 项目文档或安全管理平台；
- 两个以上独立 LLM/专家评估单元；
- 版本化对象存储或文档管理系统；
- 自动校验脚本和审批工作流。

## 2. 知识图谱

使用：

[tunnel-water-mud-inrush-resilience-kg](https://github.com/Huaiyuan-Sun/tunnel-water-mud-inrush-resilience-kg)

> 图谱 Cypher 脚本开头包含清库命令。只能导入空白或专用数据库，不得直接在包含生产数据的数据库执行。

部署后至少验证以下查询：

1. 脆弱性指标是否完整；
2. 四个恢复阶段是否可检索；
3. 规则、矩阵和策略是否连接；
4. 五个匿名案例是否可检索；
5. 策略等级是否能通过属性准确匹配。

推荐记录每次检索的查询词、节点ID、返回属性和使用目的。

## 3. 评估工作流

使用：

[tunnel-resilience-assessment-workflows](https://github.com/Huaiyuan-Sun/tunnel-resilience-assessment-workflows)

部署到 LLM 时，将工作流作为任务协议，不要求输出不受约束的内部推理。只保留：

- 证据和缺失项；
- 结构化阶段/分项结果；
- 假设和简要工程依据；
- 区间、代表值和置信度；
- 校验结果；
- 固定机器可读字段。

## 4. CI名册

CI建议分为三级，但具体正整数由项目批准：

| 级别 | 适用条件 | 项目CI |
| --- | --- | ---: |
| III | 高度适配，关键指标完整，复杂任务中稳定 | 待批准 |
| II | 基本适配，存在轻微遗漏或偏差 | 待批准 |
| I | 适配性低，规则冲突或结果不稳定 | 待批准 |

不要把模型品牌或专家职称直接等同于CI。应通过历史案例、盲评偏差、规则合规率和分任务表现确定。

## 5. 项目边界校准

论文基准边界适用于常规隧道施工情景。部署前应审查：

- 超长隧道、大断面、单通道、长距离运输和有限工作面；
- 高价值设备集中度和材料库存；
- 城市环境、敏感生态、水源保护和周边基础设施；
- 合同工期、通车目标和复工要求。

如采用项目修正系数，必须形成批准文件，说明适用范围、依据、版本和回退规则。不得在事件发生后为改变结论临时调整边界。

## 6. 离线与降级

网络或知识图谱不可用时：

1. 使用仓库内固定规则和表单；
2. 标记 `knowledge_retrieval=unavailable`；
3. 不得声称图谱验证了结果；
4. 由专家增加复核；
5. 网络恢复后补充检索并形成新版本。

计算脚本只使用 Python 标准库，可离线运行。

## 7. 数据与安全

- 原始证据区只读；
- 个人身份信息最小化；
- 未经授权不得把事故全文、照片或坐标提交给外部 LLM；
- 对外开源案例必须匿名化；
- 保存提示词版本、模型/专家标识、CI、输出和审批记录；
- 定期校验备份恢复能力。

## 8. 上线验收

- [ ] 规则与阈值经过项目总工和安全负责人批准；
- [ ] 图谱查询通过；
- [ ] 脚本测试通过；
- [ ] CI名册批准；
- [ ] 三类表单可离线填写；
- [ ] 一次桌面推演完成；
- [ ] 盲评差异和升级机制已演练；
- [ ] 数据权限和备份通过检查；
- [ ] 发布版本号和责任人已登记。

## 9. 变更、回退与年度复核

- 规则、阈值、CI、脚本或表单变更均通过版本化审批；
- 变更前后使用同一组基准案例回归测试，并记录等级与距离变化；
- 生产现场仅使用带标签的批准版本，禁止直接使用开发分支；
- 保留上一批准版本及其运行环境，确保能够回退；
- 每年至少复核一次设备能力、费用基准、环境清单、人员名册和法规适配；
- 真实事件后只更新匿名经验，不把敏感原始资料写入开源仓库。

推荐成熟度：

| 级别 | 能力 |
| --- | --- |
| M0 | 只有纸面流程，尚未演练 |
| M1 | 表单和脚本可离线运行 |
| M2 | 图谱、独立评估、审批和归档贯通 |
| M3 | 定期演练、指标监控、回归测试和持续改进 |

---

<a id="english-version"></a>

# Project Deployment Guide

## 1. Deployment profiles

The minimum offline configuration is one Python 3.9+ workstation, a read-only release of this repository, local form copies, an approved CI register, and current resource/rate/approval lead-time lists.

A standard deployment adds a Neo4j knowledge graph, a controlled document platform, two or more independent expert/LLM assessment units, versioned storage, automated validation, and an approval workflow.

## 2. Knowledge graph

Use [tunnel-water-mud-inrush-resilience-kg](https://github.com/Huaiyuan-Sun/tunnel-water-mud-inrush-resilience-kg).

> The Cypher package contains database-clearing commands. Import it only into a blank or dedicated database, never into a database containing production data.

After deployment, verify that vulnerability indicators, four recovery stages, rules, matrix relations, anonymized cases, and strategy levels are retrievable. Log each query, node/property returned, and intended use.

## 3. Assessment workflows

Use [tunnel-resilience-assessment-workflows](https://github.com/Huaiyuan-Sun/tunnel-resilience-assessment-workflows) as task protocols. Do not request unrestricted private reasoning. Retain only evidence and gaps, structured stage/component outputs, bounded assumptions and engineering rationale, intervals and confidence, validations, and fixed machine-readable fields.

## 4. CI register

Approve positive-integer CI values before an incident. Determine them from historical blind cases, task fit, rule compliance, domain competence, and repeatability rather than model brand or job title. Preserve the basis, approver, effective version, and last validation case.

## 5. Project calibration

Review whether reference boundaries remain suitable for long tunnels, large sections, single access, constrained transport, high-value equipment, urban or sensitive environmental settings, contractual milestones, and restart requirements.

Any project correction factor requires a pre-incident approval document with scope, basis, version, and rollback rule. Never change a threshold during an incident merely to change the outcome.

## 6. Offline and degraded operation

When network or graph access is unavailable:

1. use the fixed repository rules and local forms;
2. record `knowledge_retrieval=unavailable`;
3. do not claim graph validation;
4. increase qualified human review;
5. add retrieval later as a new assessment version.

The calculator uses only the Python standard library.

## 7. Data and security

- Keep original evidence read-only.
- Minimize personal information.
- Do not send full incident reports, photographs, coordinates, or contract data to an external LLM without authorization.
- Anonymize all open-source examples.
- Preserve prompt/workflow version, evaluator identity, CI, output, approval, and access logs.
- Test backup restoration, not only backup creation.

## 8. Go-live acceptance

- [ ] Rules and thresholds approved by the chief engineer and safety lead.
- [ ] Knowledge-graph queries passed.
- [ ] Calculator tests passed.
- [ ] CI register approved.
- [ ] Core forms work offline.
- [ ] One tabletop exercise completed.
- [ ] Blind-evaluator disagreement and escalation exercised.
- [ ] Access control and backup restoration passed.
- [ ] Release version and accountable owner recorded.

## 9. Change, rollback, and annual review

Version and approve every change to rules, thresholds, CI, scripts, or forms. Run the same reference cases before and after the change, recording any level or distance changes. Production uses only tagged approved releases; retain the previous approved release and runtime for rollback.

Review resource capacities, rates, environmental receptors, role registers, and regulatory fit at least annually. After a real incident, transfer only anonymized lessons to the open repository.

| Maturity | Capability |
| --- | --- |
| M0 | Written procedure only; not exercised |
| M1 | Forms and calculator run offline |
| M2 | Graph, independent assessment, approval, and archive are integrated |
| M3 | Regular exercises, metrics, regression tests, and continual improvement |
