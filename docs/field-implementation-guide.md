# 隧道施工突涌水灾害韧性评估现场实施指南

## 1. 目的、适用范围和输出

本指南用于将现场异构、缺失且不断更新的信息，转换为可复核的恢复时间、脆弱性、综合韧性等级和整改行动。适用于施工期隧道突涌水或伴随突泥、坍塌、设备受淹、环境外排的事件，也可用于事前演练和情景推演。

本指南输出：

1. 证据与缺失信息台账；
2. 恢复时间区间、代表值和1—5级；
3. 脆弱性区间、代表值和1—5级；
4. 各评估者的结构化结果与 CI；
5. 二维云模型参数、25个特征点距离和 Level I—IV 综合韧性等级；
6. 与主导薄弱项对应的措施、责任人、期限和验收证据；
7. 评估版本、审批和复评记录。

### 1.1 使用边界

- 本方法评价灾后恢复能力和后果严重程度，不预测事故发生概率。
- “可恢复性”以恢复时间操作化表示，因此数值越大，恢复能力越弱。
- 1—5级是单一维度等级，Level I—IV 是综合韧性等级，二者不得混用。
- 结果服务于资源配置和恢复决策，不替代法定责任认定、设计验算或复工审批。

## 2. 组织与职责

| 角色 | 最低职责 | 不得兼任/限制 |
| --- | --- | --- |
| 现场指挥人 | 决定安全门、资源优先级和对外发布 | 不得由自动系统替代 |
| 安全与救援负责人 | 撤人、搜救、封控、次生风险确认 | 对安全门有否决权 |
| 数据记录员 | 事件编号、证据ID、时间戳、版本归档 | 不得修改原始证据 |
| 恢复时间评估人 | A—D阶段、依赖关系和关键路径 | 应与脆弱性估算相互独立 |
| 脆弱性评估人 | LP、LC、LE分类和去重 | 不得以总损失倒推分项 |
| 造价/设备支持人 | 工程量、单价、设备修复/更换和净延误费率 | 需说明价格和时间基准 |
| 环境支持人 | 排放路径、受体、影响范围和LE等级 | 信息不足时提供等级区间 |
| 独立评估者 | 按相同证据独立出具 Time 和 Loss | 不得先查看其他评估者结论 |
| 评估负责人 | 校验、CI、云模型、签发、升级和关闭 | 对未关闭校验失败负责 |

正式部署时，建议至少设置一名隧道/地下工程专家、一名安全管理人员和一名造价或设备专业人员。LLM只能作为评估单元之一。

## 3. 部署前准备

项目开工或高风险工序开始前完成：

1. 建立本地事件目录、备份和只读原始证据区；
2. 导入配套知识图谱到空白或测试 Neo4j 数据库；
3. 校核项目适用的时间和损失边界；
4. 确定评估者名册和 CI；
5. 维护设备能力、备件、单价、运输、外援和审批时长清单；
6. 确定环境敏感受体和外排许可要求；
7. 完成桌面演练和一次盲评一致性测试；
8. 确认离线情况下仍可使用表单和计算脚本。

CI 为正整数。项目应在事件发生前，根据历史案例、规则符合度、专业经验和任务适配性确定。事件中如需调整，应保留旧值、调整理由、审批人和生效版本。

## 4. 评估总流程

### Step 0：安全门和启动

现场指挥机构确认人员安全、次生灾害控制和数据采集条件。安全门不满足时，评估状态为 `Suspended`，不得以缺少结果为由催促人员进入危险区域。

### Step 1：证据登记与缺失项识别

每项输入必须记录：

```text
Evidence ID | Value | Unit | Source | Time | Status | Owner | Used in
```

状态只允许 `Observed / Derived / Assumed / Unknown`。照片、传感器记录和口头报告应分别登记，不得把多来源合并为一条无法追溯的“综合事实”。

强制输入组：

- 项目：长度、断面、施工方法、工作面、通道、里程；
- 地质水文：围岩、断层、岩溶、水压、水源补给；
- 事件：开始时间、涌水/突泥规模、持续流量、积水/泥量；
- 人员：受影响区人数、撤离、受困、伤亡；
- 系统：供电、通风、通信、排水、支护、监测；
- 资源：水泵、管路、发电、装载、车辆、班组、备件和外援；
- 恢复：准入、加固、验证、复工审批；
- 损失：工程量、设备清单、材料、延误费率；
- 环境：外排路径、敏感受体、影响范围和持续时间。

如果关键输入缺失，先尝试用物理能力、合同、设备参数、工作面规模或正式案例建立上下界。不能建立时标记 `Unknown`，不得输出任意点估计。

### Step 2：知识图谱检索

记录查询词、返回节点、属性和用途。建议至少检索：

- `Vulnerability Assessment`
- `Recovery Time Assessment`
- `Resilience Assessment Rules`
- 与地质、涌水规模、设备受淹和环境条件相近的 `Case`
- 当前候选等级的 `StrategyLevel`

使用规则：

1. 规则用于约束计算，不证明某现场条件存在。
2. 案例只能校准或限制区间。
3. 使用案例前必须写明相似项、差异项、调整方向和幅度。
4. 检索失败时记录 `knowledge_retrieval=unavailable`，只能继续使用本次请求明确提供的规则。

### Step 3：恢复时间评估

#### 3.1 A阶段：应急响应与风险消除

包含撤离、搜救接口、封控、临时支护、封堵和防止次生灾害。A阶段只有在人员安全门和进入条件满足后才能结束。

影响因素：

- 预警和撤离路线；
- 失联、受困、坍塌和埋压；
- 通信、照明、供电和通风；
- 临时支护和反复封堵；
- 监测确认和现场准入。

#### 3.2 B阶段：排水、清淤和运输

当数据充分时：

```text
Q_eff = Q_installed × availability × operating_efficiency
Q_net = Q_eff - q_in
T_water_hours = V_water / Q_net
```

如果 `Q_net <= 0`，现有资源下排水不可完成。必须增加资源调配方案或返回 `Not assessable`，不能给出任意完成时间。

清淤：

```text
T_mud_days = V_mud / R_mud
T_mud_months = T_mud_days / 30
```

其中有效清淤能力应考虑可达性、装载、运距、班次、车辆载荷、利用率、处置和二次倒运。

#### 3.3 C阶段：设备和系统恢复

逐项分类：

- 清洗、干燥和检查；
- 现场维修；
- 更换；
- 调试和联合试运转。

必须覆盖供电、通风、排水、通信、监测、开挖、装载和运输等关键系统。备件采购和外援可与B阶段部分并行，但现场维修不得早于必要的安全准入和可达条件。

#### 3.4 D阶段：施工条件恢复与复工

包括地层加固、补充排水、防水、工法调整、监测验证、专项方案审批、人员设备重组和复工验收。对于富水破碎带、岩溶和坍塌条件，D阶段常是关键路径。

#### 3.5 重叠与关键路径

为每项活动登记总持续时间、前置条件、可并行活动和净计入阶段。优先采用关键路径法；资料不足时可用“无重叠”的保守上界，但必须明确说明。

```text
Time_low  = TA_net_low  + TB_net_low  + TC_net_low  + TD_net_low
Time_high = TA_net_high + TB_net_high + TC_net_high + TD_net_high
```

时间统一为月，默认 `1月=30日=720小时`。不舍入中间值。

#### 3.6 恢复时间分级

| Time（月） | 等级 |
| ---: | ---: |
| `[0, 0.33)` | 1 |
| `[0.33, 1)` | 2 |
| `[1, 3)` | 3 |
| `[3, 9)` | 4 |
| `[9, 24]` | 5 |

区间跨越分级边界时同时报告 `level_range`，且置信度不得为 `High`。

### Step 4：脆弱性评估

#### 4.1 人员伤亡 LP

设受物理影响区人数为 `N_affected`：

```text
LP1 + LP2 + LP3 <= N_affected
```

LP1、LP2、LP3必须是非负整数且相互排斥。已正式报告的伤亡不得被模型重新估计覆盖。上、下界应依据预警时间、撤离距离、路线阻断、埋压、照明通信和救援可达性建立，不能使用无依据的通用伤亡比例。

#### 4.2 直接经济损失 LC

每一成本项目只能归属一个分项：

- `LC1`：临时水泵/管路、动力、清淤、装运、处理和处置；
- `LC2`：设备清洗检查、维修或更换，扣除可回收价值；
- `LC3`：损坏材料、支护、管线和已完工程；
- `LC4`：净延误天数乘以净日延误费率。

```text
LC4 = non-overlapping delay duration × eligible daily delay rate
```

日费率中已包含的人工、设备待机、管理费或合同费用，若已计入LC1—LC3，必须扣除。LC统一使用万元人民币。

#### 4.3 环境影响 LE

| 等级 | 后果触发描述 | LE |
| ---: | --- | ---: |
| 1 | 基本受控，无实质生态扰动 | 0 |
| 2 | 施工区内轻微、可控、短期扰动 | 0.5 |
| 3 | 邻近区域有限污染或生态损害 | 1 |
| 4 | 大范围显著污染/损害或涉及敏感受体 | 3 |
| 5 | 广泛、严重或长期生态污染/损害 | 10 |

缺少排放路径、受体或影响范围时，应给出环境等级区间。LE映射是非线性的，应先映射上下端等级，再形成LE区间。

#### 4.4 Loss计算与分级

```text
Loss_low =
  LP1_low + LP2_low/3 + LP3_low/60
  + (LC1_low + LC2_low + LC3_low + LC4_low)/400
  + LE_low

Loss_high =
  LP1_high + LP2_high/3 + LP3_high/60
  + (LC1_high + LC2_high + LC3_high + LC4_high)/400
  + LE_high
```

| Loss | 等级 |
| ---: | ---: |
| `[0, 1)` | 1 |
| `[1, 3)` | 2 |
| `[3, 10)` | 3 |
| `[10, 30)` | 4 |
| `[30, 100]` | 5 |

`Loss_high > 100` 时保留物理估计，标记 `outside_reference_domain=true`，不得静默封顶。

### Step 5：区间、代表值和置信度

信息不完整时使用闭区间 `[lower, upper]`。上下界必须代表两个内部一致的工程情景，不能随意拼接各项最小值和最大值。

默认代表值：

```text
representative = (lower + upper) / 2
```

代表值只用于需要单值的CI融合和云模型；原区间必须进入审计记录。

置信度：

| 置信度 | 判定 |
| --- | --- |
| High | 决策关键输入均为观测或可靠推导，无主导假设 |
| Medium | 1—2个关键输入采用有边界假设，且等级在区间内稳定 |
| Low | 至少3个关键输入缺失、主导项由假设控制，或区间跨级 |
| Not assessable | 无法建立合理数值边界 |

总置信度不得高于任何主导分项的最低置信度。

### Step 6：独立评估和 CI 加权

每个评估者基于同一证据快照独立完成：

```text
evaluator_id
evidence_version
Time interval / representative
Loss interval / representative
assumptions
validation
confidence
CI
```

CI必须为已批准的正整数。计算器将CI作为样本权重，等价于按整数权重复制评估样本。不得在看到其他结论后为追求一致而修改个人结果。

出现以下情况时必须会商，但保留会商前结果：

- 任一维度最大值与最小值相差超过相邻两个分级区间；
- 某评估者存在强制校验失败；
- 结论差异来自不同事实版本；
- 主导假设相互矛盾；
- CI最高的评估者输出 `Low` 或 `Not assessable`。

### Step 7：二维云模型与综合韧性判定

每个评估者提供一对代表值 `(Time, Loss)` 和权重 `CI`。通过加权逆向云发生器计算：

```text
Ex, Ey   = 加权均值
Sx², Sy² = 加权样本方差
Enx, Eny = sqrt(pi/2) × 加权平均绝对偏差
Hex, Hey = sqrt(abs(S² - En²))
```

随后由正向云发生器生成 `(x, y, μ)` 云滴。固定随机种子，并记录云滴数，保证同一版本可重复运行。

25个韧性特征点位于五个Time区间和五个Loss区间的中点，第三维隶属度为1。分区规则：

- Level I：维度等级之和为2—3，共3个特征点；
- Level II：维度等级之和为4—5，共7个特征点；
- Level III：维度等级之和为6—7，共9个特征点；
- Level IV：维度等级之和为8—10，共6个特征点。

计算所有云滴到每个特征点的平均三维欧氏距离，最小距离对应的特征点等级为最终综合等级。自动结果必须同时保留：

- 六个云参数；
- 随机种子和云滴数；
- 25个平均距离；
- 最近特征点；
- 最近与次近距离差；
- 输入评估者、CI和证据版本。

当最近与次近距离很接近、输入区间跨级或云滴大量超出参考域时，应标记“边界敏感”，由评估负责人复核。

### Step 8：措施匹配和行动闭环

先按综合等级检索策略，再按主导分项细化：

| 综合等级 | 管理重点 |
| --- | --- |
| Level I | 保持监测、预警、演练和设备完好率 |
| Level II | 加强排水设备、备件和应急物资储备 |
| Level III | 强化超前预报、排水清淤能力、施工重组和人员支持 |
| Level IV | 优先进行地质水文调查、系统性防排水加固、冗余资源和组织整改 |

每项行动必须包含：

```text
Action ID | Trigger | Measure | Owner | Due date | Resource
Acceptance evidence | Status | Residual risk | Reassessment required
```

不得只发布“加强管理”等无法验收的措施。

### Step 9：签发、更新与关闭

最终报告至少由恢复评估人、脆弱性评估人、独立复核人和评估负责人签字。重大事故按项目和法规要求增加审批层级。

新证据、持续涌水变化、伤亡确认、设备拆检、价格变化、关键路径变化或措施完成后，应建立新版本。不得覆盖旧报告。

关闭条件：

- 所有强制校验通过或有批准的偏差说明；
- 措施已完成或转入受控的长期计划；
- 复评结果已签发；
- 原始证据、计算输入、脚本版本和审批记录已归档；
- 经验已匿名化进入案例库或明确说明不纳入原因。

## 5. 强制校验清单

### 恢复时间

- A阶段结束时人员安全门已满足；
- 持续流量不小于有效排水能力时未宣称排水可完成；
- C阶段现场维修未早于必要准入；
- D阶段包含验证和审批；
- 并行活动、调遣、等待和排水未重复计时；
- 净阶段之和复现总时间；
- 模型输入截断和物理估计均有记录。

### 脆弱性

- LP为非负整数且不超过受影响人数；
- 已报告伤亡未被覆盖；
- LC单位统一为万元；
- 每项成本只有一个归属；
- LC4使用净延误费率；
- 环境等级与LE严格一致；
- Loss算术可复现；
- 跨界和超出参考域已标记。

### 全流程

- 所有数字有单位；
- 所有假设指向其替代的缺失输入；
- 下界不大于上界；
- 代表值位于区间内；
- 图谱规则和案例未被写成现场事实；
- 未解决的校验失败在报告首页可见；
- 自动结果经过人工审批。

## 6. 停止与升级条件

出现以下任一情况，暂停自动发布并升级：

- 安全门失效或次生灾害加剧；
- 输入事实版本冲突且无法确认；
- 主导分项为 `Not assessable`；
- 伤亡约束、单位、去重或阶段加和校验失败；
- Time或Loss显著超出模型参考域；
- 结果将触发重大资源、复工或对外发布决定；
- 专家判断与模型等级存在两级或以上差异；
- 数据包含未授权的个人、事故或商业敏感信息。

## 7. 最低审计包

一次可复核评估至少保存：

```text
01_event_intake/
02_original_evidence_readonly/
03_evidence_register/
04_kg_retrieval/
05_independent_assessments/
06_calculation_input_output/
07_review_and_approval/
08_action_and_acceptance/
09_reassessment_and_closure/
```

文件名应包含事件编号、版本、时间和责任人。脚本输出应保存运行命令、代码提交号、随机种子和云滴数。

## 8. 现场决策节奏与交接

| 时间窗 | 必须形成的输出 | 责任岗位 | 允许状态 |
| --- | --- | --- | --- |
| T+0—15 min | 安全门、事件编号、首批事实、信息缺口 | 现场指挥人/安全负责人 | `Suspended` 或启动 |
| T+15—60 min | 证据台账、初始上下界、待核实清单 | 数据记录员/两类评估人 | `Provisional` |
| T+1—4 h | 独立评估、强制校验、首版行动计划 | 评估负责人 | `Provisional/Assessable` |
| T+4—8 h | 设备拆检、报价、环境及关键路径更新 | 专业负责人 | 新版本 |
| T+8—24 h | 正式复核、CI融合、云模型和审批 | 总工/评估负责人 | 批准版本 |
| 每日及重大变化后 | 措施状态、残余风险和复评 | 行动责任人 | 更新/关闭/升级 |

换班或指挥权移交时，交出方必须逐项说明安全门状态、控制性假设、未关闭校验、最近证据版本、主导关键路径、当前综合等级、待办行动和下一复评触发条件。接收方复诵确认并签署，不得只移交最终等级。

## 9. 现场数据质量分级

| 数据质量 | 最低依据 | 使用限制 |
| --- | --- | --- |
| A | 校准仪器、正式记录或两类独立来源一致 | 可用于正式上下界 |
| B | 单一可靠来源，时间和单位完整 | 可用于临时评估，需后续核验 |
| C | 有责任人的工程假设，给出物理或合同边界 | 只能形成 `Provisional` 结果 |
| D | 来源、单位、时间或对象不明 | 记为 `Unknown`，不得形成点值 |

同一数值存在冲突时，不得平均后消除冲突。应保留全部记录，优先核查量测位置、时间窗口、仪器状态、口径和单位，并以区间或多情景表示尚未解决的差异。

## 10. 敏感性与情景复核

正式签发前至少执行以下三项检查：

1. **边界检查**：分别用全部下界和全部上界运行，确认等级范围；
2. **主导项检查**：逐项缩小主要不确定区间，识别最值得补充的证据；
3. **反事实检查**：测试泵失效、持续流量上升、运输中断、设备需更换、环境等级升高或审批延迟等合理不利情景。

如果单个合理假设即可使综合等级跨越一级，标记 `boundary_sensitive=true`，措施应同时覆盖相邻两级要求。若跨越两级及以上，暂停自动签发并组织专项会商。

## 11. 行动优先级与最低响应

行动优先级由生命安全、次生灾害、关键路径、损失贡献和可实施性共同确定，不得只按综合等级机械排序。

| 优先级 | 典型条件 | 最低响应 |
| --- | --- | --- |
| P0 | 人员风险或灾害仍在发展 | 立即启动现场指挥和应急体系，暂停本指南定量流程 |
| P1 | 控制持续涌水、坍塌、通风供电或关键排水能力 | 当班明确责任人、资源和完成判据 |
| P2 | 控制恢复关键路径或主要损失贡献 | 24小时内形成批准计划 |
| P3 | 提升冗余、监测、备件、培训和长期韧性 | 纳入整改闭环和复评 |

每项措施必须具备可验证的完成定义。例如，“增加排水能力”应写明新增流量、扬程、供电、管路、安装位置、到场时间、试运行要求和验收记录。

## 12. 运行绩效指标

项目可按月或按演练统计以下指标：

- 首批事实登记完成时间；
- 关键证据具有来源、单位和时间戳的比例；
- `Assumed/Unknown` 输入比例及关闭时长；
- 强制校验一次通过率；
- 独立评估差异及会商原因；
- 结果发布前的人工审批覆盖率；
- 行动按期完成率和验收证据完整率；
- 新证据触发新版本的及时率；
- 演练中完成第一版临时评估所需时间；
- 复评后等级、区间宽度和主导项的变化。

绩效指标用于改进流程，不得用于压缩安全确认时间或鼓励无依据的精确估计。

---

<a id="english-version"></a>

# Field Implementation Guide for Tunnel Water-Inrush Resilience Assessment

## 1. Purpose, scope, and outputs

This guide converts heterogeneous, incomplete, and changing field information into reviewable recovery-time and vulnerability intervals, an integrated resilience level, and accountable improvement actions. It applies to tunnel-construction water inrush, including events accompanied by mud, collapse, equipment inundation, or environmental discharge. It may also be used for pre-incident exercises.

Required outputs are:

1. an evidence and missing-information register;
2. recovery-time interval, representative value, and dimension level;
3. vulnerability interval, representative value, and dimension level;
4. independent evaluator results and approved CI values;
5. six cloud parameters, 25 feature-point distances, and a Level I-IV result;
6. actions linked to dominant weaknesses, owners, deadlines, and acceptance evidence;
7. assessment versions, approvals, reassessments, and closure records.

### 1.1 Limits of use

- The method evaluates post-event recoverability and consequence severity; it does not predict event probability.
- Larger recovery-time values indicate weaker recoverability.
- Dimension Levels 1-5 and integrated Levels I-IV are different outputs.
- The result supports resource allocation and recovery decisions, but does not determine legal liability, design adequacy, or restart authorization.

## 2. Organization and responsibilities

| Role | Minimum responsibility | Independence or restriction |
| --- | --- | --- |
| Incident commander | Safety gate, priorities, external release | Must not be replaced by automation |
| Safety/rescue lead | Evacuation, rescue, access, secondary hazards | Holds stop authority |
| Data recorder | Incident ID, evidence IDs, timestamps, version archive | Must preserve original evidence |
| Recovery assessor | Stages A-D, dependencies, critical path | Independent from loss back-calculation |
| Vulnerability assessor | LP, LC, LE, and double-count prevention | Must not infer components from a target total |
| Cost/equipment specialist | Quantities, rates, repair/replacement, delay rate | Must state price date and basis |
| Environmental specialist | Discharge path, receptor, extent, LE interval | Uses an interval when evidence is incomplete |
| Independent evaluator | Time and Loss from the same evidence snapshot | Must not see other conclusions first |
| Assessment lead | Validation, CI, cloud model, approval, escalation | Owns unresolved validation failures |

Formal deployment should include tunnel/underground engineering, safety, cost or equipment, and environmental competence. An LLM may be one assessment unit, never the incident commander or sole approving authority.

## 3. Pre-deployment readiness

Before high-risk work:

1. establish an incident folder structure and read-only original-evidence area;
2. deploy the companion knowledge graph only to a blank or dedicated database;
3. approve time, loss, and environmental interpretation rules;
4. approve evaluators and positive-integer CI values before an incident;
5. maintain pump, power, transport, spare, supplier, external-support, and approval lead-time lists;
6. map discharge routes, permits, and sensitive receptors;
7. complete a tabletop exercise and blind consistency test;
8. prove the forms and calculator work offline.

CI is an approved task-specific weight. It must be based on historical cases, rule compliance, domain competence, and repeatability. Any incident-time change requires the old value, reason, approver, and effective version to remain auditable.

## 4. End-to-end operating procedure

### Step 0: safety gate

If evacuation, rescue, access, structural stability, ventilation, power isolation, or secondary-hazard control is not confirmed, set the assessment to `Suspended`. Never expose personnel merely to obtain a numerical input.

### Step 1: evidence and missing-data control

Each input record must contain:

```text
Evidence ID | Value | Unit | Source | Source time | Status | Owner | Used in
```

Allowed statuses are `Observed`, `Derived`, `Assumed`, and `Unknown`. Photographs, sensor records, interviews, estimates, and model outputs remain separate traceable records.

Minimum input groups cover project geometry and access; geology and hydrogeology; event timing, inflow and mud; personnel; power, ventilation, communications, drainage, support and monitoring; available resources; restart requirements; cost quantities; and environmental pathways.

When a critical value is missing, first establish a defensible physical, contractual, equipment, or case-bounded interval. If no defensible bound exists, record `Unknown` or `Not assessable`; do not invent a point estimate.

### Step 2: knowledge retrieval

Query the companion knowledge graph for vulnerability indicators, recovery stages, assessment rules, comparable cases, and candidate strategy levels. Save the query, returned node/property, purpose, and any adjustment.

Rules constrain calculations; cases calibrate or bound intervals. Neither proves a field fact. A case-based adjustment must state similarities, differences, direction, and magnitude.

### Step 3: recovery-time assessment

- **Stage A:** emergency response, evacuation interface, access control, temporary stabilization, and secondary-hazard control.
- **Stage B:** drainage, mud/debris removal, loading, transport, treatment, and disposal.
- **Stage C:** inspection, repair/replacement, commissioning, and integrated testing of critical systems.
- **Stage D:** ground treatment, waterproofing or drainage modification, method changes, monitoring verification, approvals, workforce/equipment reorganization, and restart acceptance.

When data support it:

```text
Q_eff = Q_installed × availability × operating_efficiency
Q_net = Q_eff - q_in
T_water_hours = V_water / Q_net
```

If `Q_net <= 0`, completion cannot be claimed under the current resources. Add a bounded resource scenario or return `Not assessable`.

Record every activity's gross duration, predecessor, parallel work, overlap treatment, and net stage contribution. Prefer a critical-path schedule. The auditable interval is:

```text
Time_low  = TA_net_low  + TB_net_low  + TC_net_low  + TD_net_low
Time_high = TA_net_high + TB_net_high + TC_net_high + TD_net_high
```

Use 30 days or 720 hours per month unless the project approves another conversion. Do not round intermediate values.

| Time (months) | Dimension level |
| ---: | ---: |
| `[0, 0.33)` | 1 |
| `[0.33, 1)` | 2 |
| `[1, 3)` | 3 |
| `[3, 9)` | 4 |
| `[9, 24]` | 5 |

Report a `level_range` when an interval crosses a boundary. The confidence may not be `High` in that case.

### Step 4: vulnerability assessment

Personnel components are mutually exclusive non-negative integer counts:

```text
LP1 + LP2 + LP3 <= N_affected
```

Use officially confirmed casualties where available. Do not overwrite them with model estimates.

Assign each cost once:

- `LC1`: drainage, mud removal, transport, treatment, and disposal;
- `LC2`: equipment cleaning, inspection, repair, or replacement net of recoverable value;
- `LC3`: damaged materials, support, services, and completed works;
- `LC4`: net schedule-delay duration multiplied by an eligible net daily delay rate.

All LC values use CNY 10,000. Remove labor, standby equipment, management, or contractual amounts already captured in LC1-LC3 from LC4.

Environmental consequence levels map as follows:

| Level | Operational consequence | LE |
| ---: | --- | ---: |
| 1 | Controlled; no material ecological disturbance | 0 |
| 2 | Minor, localized, short-term disturbance | 0.5 |
| 3 | Limited pollution or ecological harm outside the work area | 1 |
| 4 | Significant or wide impact, or a sensitive receptor involved | 3 |
| 5 | Extensive, severe, or long-duration ecological harm | 10 |

Calculate:

```text
Loss = LP1 + LP2/3 + LP3/60
     + (LC1 + LC2 + LC3 + LC4)/400 + LE
```

| Loss | Dimension level |
| ---: | ---: |
| `[0, 1)` | 1 |
| `[1, 3)` | 2 |
| `[3, 10)` | 3 |
| `[10, 30)` | 4 |
| `[30, 100]` | 5 |

If `Loss > 100`, preserve the physical estimate and set `outside_reference_domain=true`; do not silently cap it.

### Step 5: intervals and confidence

Use closed `[lower, upper]` intervals for incomplete information. Each endpoint must describe an internally consistent scenario. The default representative value is the midpoint and is used only for CI fusion and the cloud model; original intervals remain in the audit record.

`High` requires observed or reliable derived controlling inputs. `Medium` permits bounded assumptions when the level is stable. `Low` applies when assumptions control the result, several key inputs are missing, or the interval crosses a level. `Not assessable` applies when no defensible bound exists.

### Step 6: independent assessments and CI

Every evaluator receives the same frozen evidence version and independently reports Time and Loss intervals, representative values, assumptions, validations, confidence, and CI. Preserve pre-consensus results.

Convene a review when evaluator ranges differ by more than two adjacent dimension bands, evidence versions conflict, controlling assumptions conflict, mandatory validation fails, or the highest-CI evaluator returns `Low`/`Not assessable`.

### Step 7: two-dimensional cloud model

Use each evaluator's representative `(Time, Loss)` and positive-integer CI. The weighted backward generator estimates `Ex`, `Ey`, `Enx`, `Eny`, `Hex`, and `Hey`; the forward generator then produces `(x, y, membership)` droplets with a recorded seed and droplet count.

The 25 feature points are the midpoints of the five Time and five Loss intervals at membership 1. Their integrated bands contain 3 Level I, 7 Level II, 9 Level III, and 6 Level IV points. The feature point with the minimum mean 3D Euclidean droplet distance determines the proposed level.

Retain all 25 distances, the nearest and second-nearest points, their margin, all cloud parameters, the seed, droplet count, evaluator inputs, CI values, evidence version, and code commit. Closely spaced first/second distances, cross-level input intervals, or extensive droplets outside the reference domain require a `boundary_sensitive` review.

### Step 8: actions and closure

Match the integrated level first, then refine actions using the controlling recovery stage and largest loss contribution. Each action contains:

```text
Action ID | Trigger | Measure | Owner | Due date | Resource
Acceptance evidence | Status | Residual risk | Reassessment required
```

Do not accept non-verifiable statements such as “strengthen management.” Specify capacity, location, resources, completion criteria, and evidence.

### Step 9: approval, reassessment, and closure

At minimum, the recovery assessor, vulnerability assessor, independent reviewer, and assessment lead sign the report. New inflow data, casualty confirmation, equipment inspection, prices, critical-path changes, environmental evidence, or action completion creates a new version rather than overwriting the old one.

Closure requires resolved validations or an approved deviation, completed or controlled actions, a signed reassessment, a complete audit package, and anonymized lessons captured or formally excluded.

## 5. Mandatory validations

Confirm stage access logic, drainage feasibility, critical-path and overlap arithmetic, casualty upper bounds, integer LP values, LC units and non-duplication, LC4 net rates, LE mapping, interval ordering, representative values, domain exceedance flags, fixed seed and droplet count, all 25 distances, and human approval.

Any unresolved mandatory validation must be visible on the first page of the report.

## 6. Stop and escalation conditions

Suspend automated release when the safety gate fails; secondary hazards intensify; field facts conflict; a controlling component is `Not assessable`; casualty, unit, overlap, or arithmetic validation fails; Time or Loss materially exceeds the model domain; the result controls major resources, restart, or public release; expert and model levels differ by two or more bands; or unauthorized personal/commercial data is present.

## 7. Minimum audit package

```text
01_event_intake/
02_original_evidence_readonly/
03_evidence_register/
04_kg_retrieval/
05_independent_assessments/
06_calculation_input_output/
07_review_and_approval/
08_action_and_acceptance/
09_reassessment_and_closure/
```

File names include the incident ID, version, time, and owner. Calculator records include the command, code commit, Python version, seed, and droplet count.

## 8. Decision cadence and handover

Within 15 minutes, establish the safety gate and initial facts. Within one hour, bound missing data and controlling components. Within four hours, produce independent provisional assessments and actions. By 24 hours, complete formal review where conditions permit. Update daily and after any material change.

At shift or command handover, communicate the safety status, controlling assumptions, unresolved validations, latest evidence version, critical path, current level, open actions, and next reassessment trigger. The receiving person repeats and signs the handover.

## 9. Data-quality grades

Grade A data come from calibrated instruments, formal records, or consistent independent sources. Grade B data come from one reliable source with complete units and time. Grade C is a bounded, owned engineering assumption and supports only a provisional result. Grade D lacks source, unit, time, or object and remains `Unknown`.

Conflicting values must remain traceable. Do not average away a disagreement before checking location, time window, instrument condition, definition, and units.

## 10. Sensitivity and scenario review

Run full lower- and upper-bound cases, identify which uncertainty most changes the output, and test credible adverse scenarios such as pump failure, inflow escalation, transport interruption, equipment replacement, environmental escalation, or approval delay.

If one credible assumption moves the integrated result by one level, set `boundary_sensitive=true` and cover both adjacent action bands. A two-level movement requires escalation.

## 11. Action priority

- `P0`: active life-safety or developing-hazard condition; transfer control to the emergency command system.
- `P1`: controls inflow, collapse, ventilation, power, or critical drainage; assign owner, resources, and acceptance criteria in the current shift.
- `P2`: controls the recovery critical path or major loss contribution; approve a plan within 24 hours.
- `P3`: long-term redundancy, monitoring, spares, training, and resilience improvement.

## 12. Performance indicators

Track time to first facts, evidence completeness, assumption/unknown closure time, first-pass validation rate, evaluator dispersion, human approval coverage, action completion and evidence quality, version-update timeliness, time to provisional assessment, and change in level/interval width after reassessment. These metrics improve the process; they must never incentivize bypassing safety confirmation or fabricating precision.
