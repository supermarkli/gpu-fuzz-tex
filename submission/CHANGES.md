# TODO：
  - 等 ACM 分配 DOI/ISBN 后填入即可

### 2026-03-20

- `main.tex`：作者区从单个紧凑 `\author{...}` 块改为 `acmart` 标准逐作者元数据，同时新增 `\@mkauthors@iii` 自定义标题页渲染，以保留上标单位编号、邮箱排版和 `*`/`\dagger` 标记。

### 2026-03-19

- 将作者区改为紧凑写法：合并为单个 `\author{...}`，使用上标单位编号、合并邮箱和统一 affiliation 块。
- 更新作者单位文本为完整机构名称，并去掉所有国家信息。
- 修正 `main.tex` 中 Hongyi Lu 的机构编号为 `1,2,3`。

### 2026-03-17

- 在 `main.tex` 导言区统一设置较小的全局浮动体间距（`\textfloatsep`、`\floatsep`、`\intextsep`），以避免段落间距异常。
- 添加 DAC 2026 conference metadata：
  - `\setcopyright{acmcopyright}`
  - `\acmConference[DAC '26]{Proceedings of the 63rd Annual ACM/IEEE Design Automation Conference}{July 26--29, 2026}{Long Beach, CA, USA}`
  - `\acmBooktitle{Proceedings of the 63rd Annual ACM/IEEE Design Automation Conference (DAC '26)}`
  - `\acmYear{2026}`
  - `\acmDOI{}` 和 `\acmISBN{}`（空字段，等 ACM 分配）

### 2026-03-13

- 将项目使用的 ACM 模板从系统自带的 `acmart` v2.03 升级为项目本地的 `acmart` v2.16。
- 在当前目录新增本地模板文件 `acmart.cls` 和 `ACM-Reference-Format.bst`，确保编译优先使用最新 ACM 模板。
- 最小化清理图表周围的负 `\vspace`，减少模板版式警告并避免依赖手工压缩版面。
- 在摘要后新增 `keywords`，当前填写为 `GPU, Fuzzing, Deep Learning`。
- 添加 CCS concepts：Machine learning、Artificial intelligence、Software safety（均为 500 relevance
