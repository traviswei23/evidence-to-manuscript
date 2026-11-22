# 怎样核查交付给读者的正文

在研究项目里记录要交付的稿件、作图输入、每项关键主张的原表和具体行列、图注，以及参考文献原文定位。例子提供[模拟原始表](../examples/aperture/results.csv)、[成稿](../examples/aperture/manuscript.md)和一份[可运行的核对表](../examples/aperture/ledger.json)。把同一数值在摘要、结果、图注或结论中出现的每处写入 contexts。各条使用不同的上下文文字，含一个 `{value}`，实际稿件里保留正常书写的数值。这样只改了摘要也能找出来。

在本技能根目录运行以下命令。工具仅使用 Python 3 标准库。绝对路径调用时把 scripts 换成本技能的实际目录。

```sh
python scripts/check_manuscript.py check examples/aperture/ledger.json
python scripts/check_manuscript.py freeze examples/aperture/ledger.json --receipt audit-v1.json
python scripts/check_manuscript.py check examples/aperture/ledger.json --receipt audit-v1.json
```

| 核对表字段 | 应实际填写的内容 |
| --- | --- |
| draft、supporting_files | draft 为实际送审的 UTF-8 Markdown 或纯文本。supporting_files 列出同一案卷下审查者用到的其他文件或导出源件，按实际情况包括源代码、方法记录和补充材料。 |
| quantities | 每条有唯一 id、csv、where、column、unit_column、unit、places 和 contexts。where 用一组精确字符串定位一行，列名须唯一。原表中的数字已按所述单位表示，places 是正文的小数位，采用十进制最近舍入（正好在中间时取偶）。需换算或派生的值先保存可复算的分析及其输出，独立核原始数据，再核输出表到正文。 |
| figures | 每项给出 id、实际图片 file 和一段讨论该图的 mention，检查 Markdown 中的图片链接。另行打开图核对坐标、图例、误差量和分母。 |
| citations | 每项给出 id、正文引用片段 in_text、书目对应片段 bibliography、原始来源位置 locator，以及能支持的确切表述 supports。审稿人要实际读到指定位置。 |

退出码 0 表示登记的检查匹配。1 表示不匹配或回执过期。2 表示档案无法读取、表选中多个记录、单位不一致等输入问题。freeze 在数字和引用锚点均匹配时写入材料 SHA-256，保留已有回执。审查者收到同一版后把实际意见另存。不改变原哈希来替代审查。

对于 LaTeX、Word 或混合附件，保留源件及最终渲染稿，可在案卷里另存可查的正文导出，将源件加入 supporting_files。外部链接、TeX 图命令、复杂表格、公式、置信区间、文本未登记的数值和原文能否支撑引用，需要读者实际检查。本工具的通过只涵盖登记的稿件片段。先从全文独立清点全部核心论断，再和核对表逐项勾稽，可以发现作者漏登记的断言。

[案例复核和返修记录](../examples/aperture/review.md)展示了数值一致但措辞仍需收紧的情况。
