# 英文写作、物理段落返修与 TeX 保真

已有英文、中文待译或 TeX 原稿时，从用户指定的范围进入本页。需要从零起草时，先执行[成稿流程](manuscript-loop.md)，再对完成的章节执行下列检查。表格中的来源取自作者指定的《科研四阶段_工作流与英文写作精选》④阶段，另承接③阶段的一项工作流。

## 怎样改一节

1. **固定底稿和改动范围。** 写下具体读者、章节职责、文件及版本、作者允许改哪部分、用户要只审还是润色。只审时返回原句、诊断、依据和可选改法。润色时交可用成稿。按领域惯例建立同一个术语、符号、样本和基线对照表。中文译英文时先还原施事、比较对象、否定、条件和推断强弱，再选英文句法。[HKUST paper-polish](https://github.com/HKUSTDial/Supervisor-Skills/blob/ab4b9ceac229e84c2fecb584395af17248e7ef39/skills/paper-polish/SKILL.md#L42-L123)
2. **先论证，后句子。** 问“依照已有理解读者会预期什么，哪一项可定位结果改变这个预期？”用两句给非合作者说明问题和新答案。引言交代这一矛盾，结果给数据和适用条件，讨论回到解释及替代解释。先按稿件类型、章节功能和段间因果排序，再紧缩语言。压缩主文时保留理解结论所需的最短证据链，将只供复算的细节送补充材料。[problem-framing](https://github.com/angushushu/shu-academic-writing-skill/blob/08474025c072de67e9b52051dce5a9f2d3c8bdea/core/problem-framing/SKILL.md#L15-L79) · [nature-polishing](https://github.com/Yuan1z0825/nature-skills/blob/8a7713697d4567b3337cb20cddc55613d88f518e/skills/nature-polishing/SKILL.md#L8-L81)
3. **核准拟写的主张。** 每条重要结果先独立对照结果文件的值和出处，再问这个设计能区分哪些解释。逐项写“支持、部分支持、缺乏支持”、实际可说的条件、少了哪个对照和是否必须改变正文。材料找不到的数字先删除；部分支持的句子要写出限制。理论结果另核证明条件和极限情形。将来实验放在讨论或稿外计划。[ARIS result-to-claim，③阶段](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/result-to-claim/SKILL.md#L124-L233)
4. **长篇物理或工程段落分块处理。** 先画一条章节主线，列每段的对象、定义和作用，将依赖同一定义、公式或面板的句子放在一起。逐块检查术语漂移、不能由上一句推出的结论，以及关系代词指代。段落改序后重查第一次定义和跨段引用。最后通读整节，让另一位读者分别核物理故事和形式一致性。局部修订只复查被修改处及依赖它的段落，整节精修须覆盖全部段落。[physics-paper-editing-section](https://github.com/Harrinive/physics-paper-skills/blob/828be49d2b83750f6d2a88dedec428e8f300631e/physics-paper-editing-section/SKILL.md#L39-L92)
5. **锁住技术含义。** 对照原稿和英文成稿逐项检查 TeX 数学、上下标、引文和交叉引用键、图号、符号、正负号、数值和单位。另检查词语表达的限定，例如 `only when`、`at the four radii tested`、`under this model`、`suggest` 与 `demonstrate`。逐项说明删改某一限定是否改变适用范围。符号归一化须依作者已给的映射，另外列出修改及其所有出现位置。常规纯语言润色保留原来符号。条件不清时保留原句含义，把可能的技术改动放稿外。[paper-polisher](https://github.com/yujie-jason-zhang/polish_skill/blob/9b2a86ca6ac88879a3d3490fecdb909673fd1562/paper-polisher/SKILL.md#L22-L116)
6. **在最终成品上验收。** 起草前将作者关心的成果改成可读稿核准的条件，例如“摘要的主数值能回到原表；关键假设在第一次用公式前给出；每张核心图有正文解释”。画图、写稿、编译后按这些条件逐条验收。涉及证明时核其假设和推导，涉及定量主张时核原始数据。返修后在最终版重复关键主张、引文、渲染检查，并注明附件不足或独立评审实际未运行的部分。[ARIS paper-writing](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/paper-writing/SKILL.md#L110-L209)

## 英文 TeX 实测

将下列命令中的路径换成本次原稿、改稿和实际限定词。针对自包含 TeX 片段，它会比较常见数学环境、行内公式、引文与交叉引用的键、数值和常见单位。退出码 0 表示录入范围匹配，1 表示出现变化，2 表示材料无法比较。多文件稿件先按实际 include 链核对文件清单，再对每个实际修改的正文片段运行。遇到自定义宏、代码环境或复杂命令时打开原始 TeX 与编译件另核。保留公式的原样拼写是严格的语言改稿条件；作者明确要求改公式时单列其科学复核。

~~~text
python scripts/check_tex_edit.py examples/aperture/original-en.tex examples/aperture/edited-en.tex --keep "centered aperture" --keep "four radii tested" --keep "percentage points"
~~~

算例中把 86.47 改成 89.47、把 $a=w$ 改成 $a=2w$、把百分点换为百分比、移除只测试了四个半径的限定，都会触发相应检查。只改因果动词而保留这些字面量则可能通过，要回到原文逐句判断。见[案例复核记录](../examples/aperture/review.md)。

**给评审者的提示词**

> 逐段读原文和英文稿。把每段的对象、条件、数据、比较基准、最强结论各写一句，再查两版是否相同。只要读者能在改稿中多推出一种技术解释，就定位到具体词句。请单列程序看不出的变化，包括程度、因果、否定、分母和对既有文献贡献的归属。收到作者更正后在实际定稿中重查。

## ④阶段的 27 项怎样运行

原精选写作阶段的 20 项在本表占第 5、8、11、14、15 和 17–31 行，逐项动作和验收仍使用[原来源按项表](execution-crosswalk.md)。其余七项是第 6、7、9、10 行的四种润色流程、第 12 行的 ARIS 写作统筹、第 13 行的 ARIS 分节写作和第 16 行的问题界定。第 13 行已由[整稿循环](manuscript-loop.md)执行，其余六项在本页执行。③阶段的 result-to-claim 补上写作前检验证据的步骤。本技能因此覆盖 32 个不同的固定来源入口，其中 27 个来自④阶段。

各系统的对外投稿、自动发通知、后台持续启动、必须指定某家模型，以及专属 LaTeX 模板的排版参数，不属于通用成稿流程。原系统固定要求的盲评次数、格式或期刊标准，只在用户明确要求复现该系统或文体时按原规程执行。
