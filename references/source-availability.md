# 正文写作的来源可用性

新增 ARIS 的 paper-plan、paper-write、auto-paper-improvement-loop，以及 AutoResearchClaw 的 statistical-reporting 和 Kalaris 的 autoresearch。五个入口与原有 S17 的区别见[工作流固定提交及落点](manuscript-loop.md#四这些操作承接了哪些工作流)。下面的 342 是原精选范围的文件数。

本阶段的 20 份技能入口均已取得。每份入口按原清单指定的 GitHub 提交核对。连同直接讲解方法的文档、提示词、模板、脚本及重定位的关联材料，归集 342 个不同的仓库文件。同一文件只在本阶段计一次。文件数量仅用于复查来源。

以下记录影响复查的缺件、路径调整和容易误当原始资料的示例。每个入口的完整方法对应关系见本技能的来源对照。

| 上游入口 | 待核项目 | 核查结果与影响 |
|---|---|---|
| [paper-spine](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/skill/SKILL.md) | 已安装技能与源码路径不同 | 部分方法手册引用安装布局 scripts/…；按文件名、源码目录和 Codex 打包目录对照，取回 25 个与材料、引文、图、数值和稿件核对相关的脚本。投稿、软件更新和遥测属于其他工作，不计作写作方法。 |
| [paper-writing](https://github.com/msimchowitz/writing-skills/blob/214981fe02326f27b0fc8790d00eb4b731607073/for-agents/paper-writing/SKILL.md) | 原作者写作指南 PDF | 已定位同一提交 for-humans/human-writing-guide/human-writing-guide-main.pdf，读取 PDF 正文。技术写作规则以作者技能和指南可确认的内容为据。 |
| [paper-claim-audit](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/paper-claim-audit/SKILL.md) | 独立审查的运行材料 | ../results/run.json 在作者审查协议中用作运行数据示例，由实际项目提供。另一阶段的运行手册、监控、平台设置以及镜像没有计入正文写作的方法。 |

原文中同名的项目输入、生成文件、个人机器路径与学术书目的作用各异。凡无法从公开材料确认的指令，不以推测补写为上游原话。
