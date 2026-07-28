# 事故后快速启动卡

适用对象：现场指挥人员、项目总工程师、安全负责人和评估记录员。

## 0—15分钟：只做安全和事实登记

### 安全门

以下任一项为“否”时，暂停定量韧性评估，继续执行应急预案：

- [ ] 人员已撤离危险区，搜救状态已由现场指挥机构确认；
- [ ] 洞内进出和数据采集不会增加人员暴露；
- [ ] 供电、通风、通信、排水和支护状态已被确认或隔离；
- [ ] 持续涌水、突泥、坍塌、岩爆、有害气体等次生风险正在受控监测；
- [ ] 现场指挥人已批准启动评估。

### 建立事件编号

格式建议：

```text
项目简称-里程/工点-YYYYMMDD-序号
```

所有照片、监测数据、会议纪要、计算文件和报告必须使用同一事件编号和版本号。

### 登记首批事实

仅登记已观察或已报告内容，不推测：

- 事件时间、位置和施工工序；
- 人员数量、撤离、失联和伤亡情况；
- 瞬时/持续涌水量及泥砂情况；
- 坍塌、埋压、掌子面和支护损坏；
- 供电、通风、通信和道路状态；
- 可用水泵、管路、装载、运输和备用电源；
- 环境外排路径及敏感受体；
- 信息来源、时间戳和责任人。

使用 [`../templates/evidence-register.csv`](../templates/evidence-register.csv) 登记，每条证据赋予唯一编号。

## 15—60分钟：形成初始边界

1. 将信息标记为：
   - `Observed`：直接观测或正式记录；
   - `Derived`：由观测数据计算；
   - `Assumed`：因缺失而引入、且有工程边界；
   - `Unknown`：未知且不能安全推断。
2. 建立缺失项清单，明确每项影响恢复阶段还是损失分项。
3. 检索知识图谱中的相关规则、案例和措施；检索结果不能替代现场事实。
4. 由恢复时间评估人与脆弱性评估人分别建立初始区间。
5. 如果主导项无法建立上下界，将该分项标记为 `Not assessable`。

## 1—4小时：完成第一版可审计评估

- 填写 [`recovery-assessment.csv`](../templates/recovery-assessment.csv)；
- 填写 [`overlap-ledger.csv`](../templates/overlap-ledger.csv)；
- 填写 [`vulnerability-assessment.csv`](../templates/vulnerability-assessment.csv)；
- 完成至少两份相互独立的评估结果；
- 执行自动校验和二维云模型计算；
- 记录校验失败、边界跨越和置信度；
- 由评估负责人签发 `Provisional` 或 `Assessable` 结果。

## 更新频率

| 时点 | 最低要求 |
| --- | --- |
| T+15 min | 事件编号、安全门、首批证据 |
| T+1 h | 缺失项、初始恢复与损失边界 |
| T+4 h | 第一版结构化评估和行动计划 |
| T+8 h | 用新增监测、设备清单和报价更新 |
| T+24 h | 正式复核版本 |
| 此后每日 | 关键路径、持续流量、费用和措施状态 |
| 重大变化后 | 立即创建新版本，不覆盖旧版本 |

## 四条红线

1. 不把未知量伪装成精确点值。
2. 不把相似案例当作本项目事实。
3. 不重复计算并行工期或经济损失。
4. 不让自动结果越过安全负责人和评估负责人的审批。

## 立即升级的五种情况

- 持续流量达到或超过有效排水能力；
- 人员状态、坍塌范围或有害气体状态仍不明确；
- Time/Loss主导项无法形成工程上下界；
- 强制校验失败或专家与模型相差两级及以上；
- 结果将用于复工、重大资源调配或对外信息发布。

交接时必须口头复述并书面记录：安全门、证据版本、主导假设、未关闭校验、当前关键路径、下一更新时间和责任人。

---

<a id="english-version"></a>

# Post-Incident Quick-Start Card

Audience: incident command, chief engineer, safety lead, and assessment recorder.

## First 0-15 minutes: safety and facts only

### Safety gate

If any item is not confirmed, suspend quantitative resilience assessment and continue the emergency plan:

- [ ] Personnel have left the hazardous area and rescue status is confirmed.
- [ ] Access and data collection will not increase exposure.
- [ ] Power, ventilation, communications, drainage, and support are confirmed or isolated.
- [ ] Continuing inflow, mud, collapse, rock burst, gas, and other secondary hazards are monitored and controlled.
- [ ] The incident commander has authorized assessment start.

Create an incident ID:

```text
project-worksite/chainage-YYYYMMDD-sequence
```

Use the same incident ID and version on photographs, monitoring data, minutes, calculation files, and reports.

Register only observed or formally reported facts: time and location, work activity, personnel and evacuation status, inflow and sediment, collapse and support damage, utilities and access, available pumps and transport, discharge pathway and receptors, source, timestamp, and owner. Assign a unique evidence ID in [`../templates/evidence-register.csv`](../templates/evidence-register.csv).

## 15-60 minutes: establish initial bounds

1. Mark every input `Observed`, `Derived`, `Assumed`, or `Unknown`.
2. List missing items and the Time/Loss components they affect.
3. Retrieve relevant knowledge-graph rules, cases, and actions without treating them as field facts.
4. Recovery and vulnerability assessors independently build initial intervals.
5. Set a controlling component to `Not assessable` when no defensible bound exists.

## 1-4 hours: first auditable assessment

- Complete the recovery, overlap, and vulnerability forms.
- Obtain at least two independent assessments from the same evidence snapshot.
- Run mandatory validations and the two-dimensional cloud model.
- Record boundary crossings, failures, confidence, and the nearest/second-nearest feature points.
- The assessment lead issues only an `Assessable` or `Provisional` result that has passed the required review.

## Update cadence

| Time | Minimum output |
| --- | --- |
| T+15 min | Incident ID, safety gate, initial evidence |
| T+1 h | Missing data and initial Time/Loss bounds |
| T+4 h | First structured assessment and action plan |
| T+8 h | Updated monitoring, inspection, price, and environment data |
| T+24 h | Formally reviewed version |
| Daily | Critical path, continuing inflow, costs, and action status |
| Material change | Immediate new version; never overwrite the old one |

## Four red lines

1. Never disguise an unknown as a precise point.
2. Never present a similar case as a project fact.
3. Never double-count parallel duration or loss.
4. Never let an automated result bypass safety and assessment approval.

## Immediate escalation

Escalate when continuing inflow meets or exceeds effective drainage; personnel or secondary-hazard status is unresolved; a controlling Time/Loss component cannot be bounded; mandatory validation fails; expert and model levels differ by two or more bands; or the result will control restart, major resources, or public release.

At handover, repeat and record the safety status, evidence version, controlling assumptions, open validations, critical path, next update, and responsible person.
