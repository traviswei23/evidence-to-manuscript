# 稿件材料的专项核查

按眼前的疑点选一项执行。某项核查能改变数值、主张范围、读图方式或交付文件时，才把发现写给作者。

## 有两套数据或两版图时，先辨认它们来自哪次研究

1. 给候选材料各写一句身份说明，包括实验或推导、条件、处理版本、指标定义、对应面板。文件同名、修改时间较晚，只能帮助寻找版本。
2. 先用实验记录和作者指定版本筛出身份相符的候选。例如，一张更新的归一化曲线不能直接替换旧稿中报告绝对值的曲线。身份相同但数值不同，查生成脚本、结果列与导出设置；判断不清就只暂停受影响的句子。
3. 对需要交付的最终图，把可编辑源图、源数据、出版用图片和最终稿中的落点各记一处。多轮改图时给已审版本编号或保存内容指纹。替换最终图后，用相同页面、裁切区域和显示尺寸并排看两版；重新核对变动面板、首引段落和图注。若只交文字，可以跳过版面操作。[材料版本选择](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/asset_selection.py)、[保留图版与指纹](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/preserve_figure_revision.py)、[同位置并排比较](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/figure_comparison.py)、[图与正文的对应检查](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/figure_story_check.py)。

## 一句同时引用本研究结果和外部论文时，分开核证

逐个圈出句中的动作、比较和解释。给每一项写“本研究结果编号或文献身份、准确位置、实际能支持的内容”。例如，“B 的误差下降，说明过程 X 得到了抑制”包含两个判断。误差表可以证实降幅。即使一篇前作报告了 X 受抑制，还需判断它的条件与本研究是否可比，以及本研究是否测过 X。缺少后一项时，将机制改写为待检验解释，把引文放在它确实支持的分句之后。[主张、结果和来源的关联](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/scientific_evidence_check.py)、[引文对应的具体句子](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/citation_bank_check.py)。

同一来源存在多个版本时，先用 DOI，再用规范题名、作者和年份认定身份，核实实际引用的是哪一版。若有人说“文章没有报告这个条件”，记录查过的主文、补充文件、表格和关键词。全文不可得时，将结论限定到查过的材料。真实检索无结果、检索服务出错、仅核实书目信息分别记录。[书目身份核验](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/citation_verification_en.py)、[可定位的缺失证据记录](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/evidence_grounded_review.py)。

## 润色、改写或翻译后，检查科学信息有没有悄悄改变

把原稿和新稿放在一起，逐段比对数字与单位、公式和符号、引文、术语、否定及适用条件。对同一个数值或术语多次出现的情况，同时检查次数及其所在分句。全稿总数没变，数值仍可能移到了另一个组或条件。变动处注明作者要求的改动及其依据。[数字、公式和术语核对](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/author_voice_check.py)、[翻译结构核对](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/translate_guard.py)。

要求改论证时，将改动最大的段落与最接近的旧段落配对，检查有没有丢失限定；将几乎未改的段落与要求修复的问题配对，检查是否漏改。段落相似度用于定位人工核查的位置。若改动只为澄清语句，重读首次提出结论的那一句，把决定其真假的条件放在该处，避免读者到讨论末尾才发现限制。[段落重排与变更对照](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/revision_audit.py)、[原作者技术写作指南，第 5–6、9 节](https://github.com/msimchowitz/writing-skills/blob/214981fe02326f27b0fc8790d00eb4b731607073/for-humans/human-writing-guide/human-writing-guide-main.pdf)。

## 可编辑稿和导出版有差异时，在实际交付版本中核对

抽取一个容易出错的对象，从源稿跟到最终交付物。例如核对一条带负号和下标的公式、一张多面板图，或一句带引文的定量比较。检查源稿中的是什么意思、导出版上实际显示什么，以及交叉引用最终跳到哪里。若修改 Word 中的公式或插图，保留可编辑原件，再复核断行、符号、图的尺寸和清晰度。重编 PDF 或更换图文件后，先前的页面核查只对原版本有效。[LaTeX 与引文键核对](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/latex_guard.py)、[Word 中的图和文本](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/word_guard.py)、[最终 PDF 的实际页面](https://github.com/WUBING2023/PaperSpine/blob/f68989ccea75312d57884e0c1df423b77fb4ba3c/src/scripts/visual_readiness_check.py)。

交给作者的异常记录只需写明“哪一句或哪一面板、比较了哪两个输入、发现了什么、已经改到哪里、还需谁判断”。若需要确认缺失的仪器参数或有分歧的数据版本，给出它们各自会改变的结论。
