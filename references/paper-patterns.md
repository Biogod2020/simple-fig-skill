# 范文模式：具体参考了谁、哪张图、借鉴什么

这是 2026-09-14–15 制图审阅中已检查原文图页与图注的**回顾性设计索引**。本次技能更新整理已有阅读记录，并非重新开展系统综述，也不声称逐一复核了每篇独立补充文件或当前最新发表状态。页码按当时 PDF 从 1 开始计数；版本不同可能换页，应以图号核对。

NBME 指 **Nature Biomedical Engineering**。Nature Methods、ICLR、NeurIPS 与预印本分别标注；不因“知名团队/大佬组”称呼而自动赋予方法或审美权威。期刊归属能核对，团队背景若是新任务所需则另外核实，不用宣传性标签代替来源。

## 13 篇原文及可迁移的设计

| 来源与所用版本 | 具体原图/位置 | 实际借鉴的形式 | 不能据此推出 |
|---|---|---|---|
| [BioMedAgent](https://www.nature.com/articles/s41551-026-01634-6)，NBME 2026 | Fig.1a，p.3；Fig.4，p.8 | 机器人充当有连线的流程角色；总体架构之后放大局部机制，再与该机制的热图/定量评测并置。 | 不能给单 agent 项目添加其多 agent、记忆更新或自学习能力。 |
| [DSWizard / BioDSA 论文](https://www.nature.com/articles/s41551-025-01587-2)，NBME 2026；题名 *Making large language models reliable data science programming copilots for biomedical research* | Fig.3a，图 p.7、图注 p.6；同图 b–g | agent、工具、执行环境各有角色；具体操作小图和准确率、难度、资源等结果共享一图。短操作名就地标注。 | 不能把它的工具增益移植到另一工作流；不代表所有工程过程都应占一整张主图。 |
| [spEMO](https://www.nature.com/articles/s41551-025-01602-6)，NBME 2026 | Fig.1a–b，p.3；Fig.2，p.4；Table 1，p.13 | 表达、图像与编码对象可辨；实际空间图和常规定量比较并排；精确分数可进入正式表。 | 它是多模态方法参照，不是收集 agent 的直接同类；不能凭配色创造空间分区或模型结果。 |
| [XunZi](https://www.nature.com/articles/s41551-026-01769-6)，NBME 2026 | Fig.1a，图 p.3、图注 p.2；Figs.2–4 | 推理/多模态对象之后接实际预测与实验验证，让技术和科学意义相连。 | 不支持“所有后续图都继续展开工程架构”，也不能借用它的生物学发现。 |
| [SpatialData](https://www.nature.com/articles/s41592-024-02212-x)，Nature Methods，在线 2024 / 卷期 2025 | Fig.1，p.2；Fig.2，图 p.3、图注 p.4 | 数据对象、操作和坐标变换先抽象表示，再用真实多模态空间对象与配准解释关系。 | 文件后缀本身不足以解释方法；对象关联线不应误表示数据生成关系。 |
| [CellAgent](https://proceedings.iclr.cc/paper_files/paper/2026/hash/7c482acecdd1b3386a3a11acc536a22a-Abstract-Conference.html)，ICLR 2026 | Fig.1，p.3；Table 1，p.6；附录 Figs.10–12，pp.28–30 | 主图保留任务、工具、执行和评价核心循环；完整提示词、异常和代码修复在附录展开。 | ICLR 论文不能充当 NBME 制版规范；主图不必塞满日志。 |
| [ScienceAgentBench](https://proceedings.iclr.cc/paper_files/paper/2025/hash/f12b4df26344f3be803c06b555252efe-Abstract-Conference.html)，ICLR 2025 | Fig.2，p.3；Figs.3–4，pp.9–10 | 用任务要求、数据预览、知识和参考程序使评测对象具体；区分执行、阶段正确性与任务成功。 | 可执行/好看不等于科学任务成功；不同评测分母不能拼成一个成功率。 |
| [SWE-agent](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html)，NeurIPS 2024 | Fig.3，p.4；附录 Figs.10–13 | 当接口本身是贡献，主图可以展示真实文件观察、编辑调用和修改后状态；完整配置留在附录。 | 不能制定“主图一律不许技术名/代码”的绝对规则；无关内部代号仍应翻译。 |
| [HEST-1k](https://proceedings.neurips.cc/paper_files/paper/2024/hash/60a899cc31f763be0bde781a75e04458-Abstract-Datasets_and_Benchmarks_Track.html)，NeurIPS 2024 Datasets and Benchmarks | Fig.1b，p.2；Fig.3，p.9 | legacy readers 接具体每样本产物；真实组织图、区域视图和定量信息紧密组合，比例尺贴图。 | 资源规模不是独立验证结果，也不能转用它的下游应用收益。 |
| [Biomni](https://www.biorxiv.org/content/10.1101/2025.05.30.656746v1)，2025-06-02 preprint v1 | Fig.1a，p.15；Fig.3，p.17 | 行动空间、环境、观察循环及克制角色图标；真实任务输入、分析步骤和输出图件构成一个可跟踪案例。 | 不混用后续发表版本；示意或跨条件案例不能冒充同一次成功修复轨迹。 |
| [scBaseCount](https://doi.org/10.1101/2025.02.27.640494)，所用 2025-11-02 预印本 | Fig.2A–F，pp.5–6 | 发现/元数据整理、统一计数、工具层级和标签对照共同出现，是“工程机制 + 验证”较直接的先例。 | 不照搬多 agent 层级；它使用技术名称不意味着应搬入另一项目所有函数。 |
| [MetaMuse](https://doi.org/10.64898/2026.04.12.718044)，所用 2026-04-20 预印本 | Fig.1、Table 1，p.4；Figs.2–4 | 来源/样本类型、字段整理、仲裁和规范化分层，后续对相应任务分开评估。 | 不把一次联合判断拆成未实现的多阶段 agent；不据此假设后续正式发表状态。 |
| [GEOMeta](https://doi.org/10.64898/2026.08.19.745739)，所用 2026-08-20 预印本 | Fig.1B，p.5；Methods，pp.31–33 等 | 准备、提取、质控、标准化、映射与输出清楚连接；身份/数量保持原则可见，完整 schema 和批次恢复留在 Methods。 | 不复制其完整流程；不把来源缺失画成负面证据，也不假设每个阶段都是独立模型调用。 |

MetaMuse、GEOMeta、scBaseCount 的当时在线 DOI 访问未成功，图件判断来自已保存的带版本/日期 PDF；这些链接是来源标识，不是本次成功下载或后续发表的保证。Biomni 明确使用 v1。NBME 部分原文通过作者提供的正式版 PDF 检查。未来若需要最新版本，应重新取得并核对，不沿用旧页码冒称已看过新稿。

## 按设计问题找范文

| 要修复的问题 | 优先比较的具体形式 |
|---|---|
| Fig.1 太抽象，agent 不像实际操作者 | BioMedAgent Fig.1a、DSWizard Fig.3a：对象明确，角色进入数据/反馈路径。 |
| 后续图重复总览 | BioMedAgent Fig.4、DSWizard Fig.3：只展开一个局部机制，并给该机制的证据。 |
| 不知道工程细节该不该进主图 | SWE-agent Fig.3、scBaseCount Fig.2：若接口/处理决定方法能力，就画实；CellAgent 附录限定全文日志的深度。 |
| 只有文字流程，没有具体空间内容 | SpatialData Fig.2、spEMO Fig.2、HEST Fig.3：真实图像、坐标/对象关系与可比量化组合。 |
| 质检/审阅/执行的“成功”混在一起 | ScienceAgentBench Figs.2–4：先定义任务与不同评价层次，再画结果。 |
| 表格太多、图型过于一致 | DSWizard Fig.3、BioMedAgent Fig.4、spEMO Fig.2/Table 1：机制、矩阵、散点、曲线和正式表各有职责。 |
| 视觉漂亮但缺少意义 | Biomni Fig.3、XunZi Figs.2–4：从真实问题连接过程、可见产物和验证。 |

这是按功能匹配的设计推断；没有据此计算“多少篇都这么画”，也不声称所有范文都用环形图、同一配色或同一流程占比。

## 如何做一次可信的交叉比较

1. 选与目标 panel **功能相同**的原图，记录论文、来源类别、所用版本、图号/页码及原文链接；可用时记录 PDF 哈希。
2. 检查实际原图和图注。比较对象、短标签位置、角色/连线语义、机制与数据分工、真实图像占比和最终字号；不凭摘要推测版式。
3. 在自己的设计记录中写清“采用什么、对应哪个 panel、哪些能力/数据不能借用”。借鉴组织方法，不复制原图、图标、文字或实验数值。
4. 同宽对照可帮助看构图；原文和新稿的原生/最终物理字号另查。若用户要求全套比较，覆盖每张主图，而非只检查 Fig.1。
5. 审阅对照文件与投稿图件分开。只有用户要求时制作 HTML 或对照册；本 skill 不打包这些论文的 PDF/截图。

期刊正式要求要另查当前的作者/制图指南。这份索引解释设计依据，不能认证达到 NBME 审美门槛或保证 ICLR/NBME 录用。
