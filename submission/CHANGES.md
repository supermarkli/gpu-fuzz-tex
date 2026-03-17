todo：
  - 无（camera-ready 准备就绪，等 ACM 分配 DOI/ISBN 后填入即可）

2026-03-17

- 添加 DAC 2026 conference metadata：
  - `\setcopyright{acmcopyright}`
  - `\acmConference[DAC '26]{Proceedings of the 63rd Annual ACM/IEEE Design Automation Conference}{July 26--29, 2026}{Long Beach, CA, USA}`
  - `\acmBooktitle{Proceedings of the 63rd Annual ACM/IEEE Design Automation Conference (DAC '26)}`
  - `\acmYear{2026}`
  - `\acmDOI{}` 和 `\acmISBN{}`（空字段，等 ACM 分配）

2026-03-13

- 将项目使用的 ACM 模板从系统自带的 `acmart` v2.03 升级为项目本地的 `acmart` v2.16。
- 在当前目录新增本地模板文件 `acmart.cls` 和 `ACM-Reference-Format.bst`，确保编译优先使用最新 ACM 模板。
- 最小化清理图表周围的负 `\vspace`，减少模板版式警告并避免依赖手工压缩版面。
- 在摘要后新增 `keywords`，当前填写为 `GPU, Fuzzing, Deep Learning`。
- 添加 CCS concepts：Machine learning、Artificial intelligence、Software safety（均为 500 relevance

