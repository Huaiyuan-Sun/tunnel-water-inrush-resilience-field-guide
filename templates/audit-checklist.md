# 强制审计清单

## 基本控制

- [ ] 事件编号、证据版本和评估版本一致
- [ ] 原始证据为只读并保留来源与时间
- [ ] 每个数字都有单位
- [ ] 每个假设指明替代的缺失输入
- [ ] 下界不大于上界
- [ ] 代表值位于区间内
- [ ] 图谱规则和案例未被表述为现场事实

## 恢复时间

- [ ] A阶段结束前人员安全门已满足
- [ ] `Q_net <= 0` 时未给出无资源依据的排水完成时间
- [ ] C阶段现场维修未早于必要准入
- [ ] D阶段包含验证和复工审批
- [ ] 并行活动按关键路径只计算一次
- [ ] A+B+C+D复现总时间
- [ ] 超过24个月的物理估计和模型输入均已记录
- [ ] 跨级区间未标记为High confidence

## 脆弱性

- [ ] LP为非负整数
- [ ] LP总数不超过受影响人数
- [ ] 已正式报告的伤亡未被覆盖
- [ ] LC统一使用万元
- [ ] 每项成本只有一个归属
- [ ] LC4使用净延误费率
- [ ] 环境等级与LE完全一致
- [ ] Loss上下界算术可复现
- [ ] `Loss > 100` 已标记超出参考域

## 多评估者与云模型

- [ ] 评估者使用相同证据快照并独立评价
- [ ] CI来自已批准名册且为正整数
- [ ] 会商前结果已保留
- [ ] 随机种子、云滴数和代码版本已记录
- [ ] 25个特征点距离均已保存
- [ ] 最近和次近特征点差异已检查
- [ ] 自动等级经过评估负责人审批

## 行动与关闭

- [ ] 每项措施有责任人、期限和验收证据
- [ ] 主导薄弱项与措施对应
- [ ] 未关闭校验失败在报告首页可见
- [ ] 新证据触发了新版本而非覆盖
- [ ] 关闭前已完成复评和归档

审计结论：`Pass / Fail / Conditional`

未关闭事项：

复核人：

日期：

---

<a id="english-version"></a>

# Mandatory Audit Checklist

## Basic controls

- [ ] Incident ID, evidence version, and assessment version are consistent.
- [ ] Original evidence is read-only with source and timestamp.
- [ ] Every number has a unit.
- [ ] Every assumption identifies the missing input it replaces.
- [ ] Lower bounds do not exceed upper bounds.
- [ ] Representative values lie within intervals.
- [ ] Knowledge-graph rules and cases are not presented as field facts.
- [ ] Conflicting evidence and resolution are retained.

## Recovery time

- [ ] The personnel safety gate is satisfied before Stage A closes.
- [ ] No drainage completion is claimed when `Q_net <= 0` without an added resource scenario.
- [ ] On-site Stage C repair does not precede safe access.
- [ ] Stage D includes verification and restart approval.
- [ ] Parallel work is counted once through a dependency/overlap ledger.
- [ ] A+B+C+D reproduces total Time.
- [ ] Physical Time above 24 months and model input are both recorded.
- [ ] A boundary-crossing interval is not reported with `High` confidence.

## Vulnerability

- [ ] LP values are non-negative integers.
- [ ] Total LP does not exceed affected personnel.
- [ ] Official casualty records are not overwritten.
- [ ] All LC values use CNY 10,000.
- [ ] Each cost has one category only.
- [ ] LC4 uses a net eligible delay rate.
- [ ] Environmental level maps exactly to LE.
- [ ] Loss lower/upper arithmetic is reproducible.
- [ ] `Loss > 100` is flagged outside the reference domain.

## Multiple evaluators and cloud model

- [ ] Evaluators used the same evidence snapshot independently.
- [ ] CI is a positive integer from the approved register.
- [ ] Pre-consensus results are preserved.
- [ ] Seed, droplet count, code version, and command are recorded.
- [ ] All 25 feature-point distances are saved.
- [ ] Nearest and second-nearest distance margin is checked.
- [ ] A boundary-sensitive result receives human review.
- [ ] The proposed automated level is approved by the assessment lead.

## Actions and closure

- [ ] Every action has owner, deadline, resources, and acceptance evidence.
- [ ] Actions address controlling weaknesses.
- [ ] Open validation failures appear on the report first page.
- [ ] New evidence created a new version instead of overwriting.
- [ ] Handover records include assumptions, validations, and next triggers.
- [ ] Reassessment and archive are complete before closure.

Audit result: `Pass / Fail / Conditional`

Open items:

Reviewer:

Date:
