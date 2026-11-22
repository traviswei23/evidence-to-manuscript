# 从研究证据写到正文

一个用于 Codex 的中文科研技能。从作者已有结果、图表、实验记录和参考文献起草中文或英文论文，支持单节、整稿、图序重组与数值复核。

将本仓库放入论文项目的 `.agents/skills/evidence-to-manuscript/`。在项目中明确调用：

> $evidence-to-manuscript 用我的最终结果表、图 2 和图 3 及图注，先写 Results。逐项核对比较对象和样本数，把数据不能回答的问题列在稿外。

完整写作会给出所请求的可编辑正文、关键主张对应的证据，以及影响使用的未决问题。已有方案或查新报告可以作为输入，也可直接从图表开始。

- [技能入口](SKILL.md)
- [英文分节改稿、TeX 保真工具与④阶段 27 项的对应关系](references/english-revision.md)
- [从证据到成稿、独立复核和返修的执行流程](references/manuscript-loop.md)
- [可复跑的数值光学论文样例](examples/aperture/manuscript.md)与[回查原表的操作](references/verification.md)
- [原有 20 个来源的实际用法](references/execution-crosswalk.md)及[新增五个工作流与固定来源](references/manuscript-loop.md#四这些操作承接了哪些工作流)
- [可复用提示词和算例](references/prompts.md)
- [20 个原始技能的来源和方法对照](references/source-map.md)

[上游固定版本、可用附件与缺件说明](references/source-availability.md)
