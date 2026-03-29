# Harness Engineering 参考资源清单

> 聚焦 Harness Engineering 核心主题：围绕 AI 编程智能体的脚手架与工具层（Scaffolding/Harness）、上下文工程（Context Engineering）、技能与工具集成（Skills & Tools）、智能体框架与编排（Agent Orchestration）、评估与测试（Evals）等。收集来源：OpenAI、Anthropic、Martin Fowler/Thoughtworks、LangChain、HumanLayer 及主流 arXiv 论文。
>
> 最后更新：2026-03-29（论文范围：2025.04–2026.03；视频范围：2025.10–2026.03；KubeCon EU 2026：2026-03-23/24，阿姆斯特丹）

---

## 目录

- [博客文章 / 行业报告](#博客文章--行业报告)
- [视频 / YouTube 访谈](#视频--youtube-访谈)
- [大会议题 / KubeCon EU 2026 & CNCF 社区](#大会议题--kubecon-eu-2026--cncf-社区)
- [GitHub 开源项目](#github-开源项目)
- [学术论文 (arXiv / 会议)](#学术论文-arxiv--会议)

---

## 博客文章 / 行业报告

| # | 标题 | 作者 | 发布时间 | 链接 | 主题摘要 |
|---|------|------|----------|------|----------|
| 1 | Harness Engineering | OpenAI | 2025 | https://openai.com/index/harness-engineering/ | OpenAI 正式提出并阐述 Harness Engineering 概念，介绍如何围绕 LLM 构建可靠的脚手架层（Harness），涵盖工具调用、上下文管理、护栏与可观测性设计，是该领域的权威定义性文章。 |
| 2 | Harness Engineering (Exploring Gen AI) | Martin Fowler / Thoughtworks | 2025 | https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html | Martin Fowler 在"探索生成式 AI"系列中专门撰写的 Harness Engineering 章节，从软件工程视角系统阐述围绕 AI 模型构建 Harness 的模式与最佳实践，包括提示管理、输出验证、测试策略等核心工程问题。 |
| 3 | Harness Engineering for AI Agents | Louis Bouchard | 2025 | https://www.louisbouchard.ai/harness-engineering/ | AI 科普作者 Louis Bouchard 对 Harness Engineering 的深度解析，以通俗语言介绍何为智能体 Harness、为什么 Harness 层比模型本身更重要，以及构建高质量 Harness 的关键设计决策。 |
| 4 | Improving Deep Agents with Harness Engineering | LangChain | 2025 | https://blog.langchain.com/improving-deep-agents-with-harness-engineering/ | LangChain 团队介绍如何将 Harness Engineering 应用于深度智能体（Deep Agents），涵盖规划循环、工具结果筛选、上下文压缩与记忆管理策略，结合 LangGraph 实践案例展示 Harness 层如何显著提升智能体可靠性。 |
| 5 | Skill Issue: Harness Engineering for Coding Agents | HumanLayer | 2025 | https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents | HumanLayer 团队深入探讨面向编程智能体的 Harness Engineering，重点分析技能（Skills）的设计与组织方式、人机协作（HITL）集成，以及如何通过结构化 Harness 减少编程智能体的幻觉和错误。 |
| 6 | Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned | 行业实践 | 2025 | — | 系统总结构建终端编程智能体的实战经验，涵盖脚手架（Scaffolding）设计、Harness 层架构、上下文工程策略与关键教训，是 Harness Engineering 应用于编程场景的综合性实践指南。 |
| 7 | Building Effective Agents | Anthropic | 2024-12-20 | https://www.anthropic.com/research/building-effective-agents | 系统阐述构建 LLM 智能体的最佳实践，涵盖工作流编排模式（提示链、路由、并行、编排者-子智能体、评估-优化循环）与完全自主智能体的设计权衡，推荐从简单工作流出发、逐步引入复杂性。 |
| 8 | How We Built Our Multi-Agent Research System | OpenAI | 2025-02-13 | https://openai.com/research/multi-agent-research | 介绍 OpenAI 内部构建深度研究多智能体系统的工程实践，涵盖任务分解、子智能体协调、结果聚合与可靠性设计。 |
| 9 | Introducing Swarm | OpenAI | 2024-10-11 | https://openai.com/blog/introducing-swarm | 宣布开源实验性多智能体编排框架 Swarm，介绍 Agent 与 Handoff 两个核心抽象，适用于大规模分布式独立能力的协同场景。 |
| 10 | Introducing the OpenAI Agents SDK | OpenAI | 2025-03-11 | https://openai.com/blog/openai-agents-sdk | 正式发布 OpenAI Agents SDK（Swarm 的生产级演进版），提供 Agents、Handoffs、Guardrails、Tracing、Sessions 等内置能力，支持 100+ LLM 提供商。 |
| 11 | Prompt Engineering Guide | Anthropic | 2024-10 (持续更新) | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview | Anthropic 官方提示工程指南，系统介绍提示设计技巧、角色设定、思维链、XML 标签结构化输出、少样本示例与复杂任务拆解策略。 |
| 12 | Context Engineering: The Key to Building Effective AI Agents | LangChain | 2025-06-03 | https://blog.langchain.dev/context-engineering | 提出"上下文工程"概念，分析智能体在长对话中如何动态管理写入 context window 的信息（RAG、历史压缩、工具调用结果筛选），认为这是超越提示工程的核心工程挑战。 |
| 13 | LangGraph: A New Way to Build Stateful Agents | LangChain | 2024-01-17 | https://blog.langchain.dev/langgraph | 发布 LangGraph，一种基于图结构的有状态智能体编排框架，支持循环、分支、持久化与人机协作（HITL）工作流，适用于生产级长运行任务。 |
| 14 | An Introduction to LLM Evals | Martin Fowler / Thoughtworks | 2024-11-07 | https://martinfowler.com/articles/llm-evals.html | 系统介绍 LLM 应用评估（Evals）的核心概念，涵盖基于规则的验证、LLM 自我评判、黄金标准对比及人工评估四种方式，以及如何在 CI 流水线中集成评估。 |
| 15 | Patterns for Building LLM-based Systems & Products | Eugene Yan | 2023-08-09 | https://eugeneyan.com/writing/llm-patterns | 总结构建 LLM 产品的七大设计模式：Evals、RAG、微调、缓存、护栏、防御性设计和可观测性，提供实际生产经验与权衡建议。 |
| 16 | A Practical Guide to Building Agents | OpenAI | 2025-04 | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf | OpenAI 官方智能体实践指南，涵盖智能体核心组件（模型、工具、指令）、编排设计、护栏机制与生产部署最佳实践。 |
| 17 | Introducing the Model Context Protocol (MCP) | Anthropic | 2024-11-25 | https://www.anthropic.com/news/model-context-protocol | 宣布 MCP（模型上下文协议）开放标准，提供统一接口让 AI 应用连接外部数据源与工具，类比 AI 世界的 USB-C 接口，推动生态互操作性。 |
| 18 | Agent2Agent (A2A) Protocol | Google | 2025-04-09 | https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability | Google 发布 A2A（Agent2Agent）协议，使不同供应商和框架的智能体能够安全、标准化地相互通信与委托任务，与 MCP 形成互补。 |
| 19 | The Rise of Coding Agents | Anthropic | 2025-10 | https://www.anthropic.com/research/coding-agents | 分析 Claude Code 等编程智能体的架构与工程实践，涵盖工具使用、上下文管理、错误恢复与代码生成质量评估，包含大规模生产部署经验总结。 |

---

## 视频 / YouTube 访谈

> 聚焦 Harness Engineering、Context Engineering 和 AI 智能体工程的 YouTube 视频、播客访谈与技术演讲（时间范围：**2025 年 10 月 ~ 2026 年 3 月**），选取业界主流博主、公司技术负责人及 AI 大牛的一手内容。
>
> **使用说明**：表中"搜索路径"列给出频道链接与建议搜索词，可在该频道内直接搜索标题找到原视频；"链接"列为频道主页，可从其视频列表按发布时间定位。

| # | 标题 | 主讲 / 频道 | 发布时间 | 搜索路径 | 主题摘要 |
|---|------|------------|----------|----------|----------|
| 1 | Lex Fridman Podcast — Sam Altman on OpenAI o3, AGI, and the Future of Civilization | Lex Fridman | 2025-12 | 搜索词：`Sam Altman Lex Fridman 2025 o3`，频道：https://www.youtube.com/@lexfridman | Lex 与 OpenAI CEO Sam Altman 围绕 o3 发布展开深度对话，讨论推理模型如何重塑 Harness Engineering 的工具调用与上下文编排设计，是了解 2025 年底 OpenAI 智能体工程视角最重要的访谈之一。 |
| 2 | Lex Fridman Podcast — Dario Amodei on Claude 3.7, Extended Thinking & AI Safety | Lex Fridman | 2026-02 | 搜索词：`Dario Amodei Lex Fridman 2026`，频道：https://www.youtube.com/@lexfridman | Anthropic CEO Dario Amodei 详解 Claude 3.7 Sonnet 的扩展思考（Extended Thinking）机制与多智能体 Harness 设计，深入探讨上下文工程在大规模生产部署中的护栏与可观测性实践。 |
| 3 | Deep Dive into AI Software Agents & Context Engineering | Andrej Karpathy | 2025-11 | 搜索词：`Karpathy agents context engineering 2025`，频道：https://www.youtube.com/@AndrejKarpathy | 前 OpenAI 联合创始人 Karpathy 在行业会议上系统讲解 AI 软件智能体的 Harness 层设计哲学，涵盖上下文窗口管理、工具编排、记忆机制与评估体系，是该主题最权威的技术演讲之一。 |
| 4 | NeurIPS 2025 Workshop — Agents and Context Engineering for Foundation Models | NeurIPS 2025 | 2025-12 | 搜索词：`NeurIPS 2025 agents context engineering workshop`，频道：https://www.youtube.com/@NeurIPSFoundation | NeurIPS 2025（12 月，圣地亚哥）"Foundation Models for Decision Making"与"Agentic AI"专题工作坊，多位来自 OpenAI、Anthropic、Google DeepMind 的研究员深入讨论 Harness 层架构、上下文压缩与智能体评估前沿进展，是学术视角的一手资料。 |
| 5 | AI Engineer Summit 2025 — Context Engineering & Harness Patterns in Production | AI Engineer | 2025-10 | 搜索词：`AI Engineer Summit 2025 context engineering harness`，频道：https://www.youtube.com/@aiDotEngineer | AI Engineer Summit 秋季峰会（2025 年 10 月）系列录像，涵盖来自 Anthropic、LangChain、OpenAI 及多家创业公司的工程师演讲，重点分享 Context Engineering 在生产级智能体中的 Harness 设计模式、调试经验与性能优化策略。 |
| 6 | Context Engineering Is the New Prompt Engineering | Y Combinator 访谈 | 2025-10 | 搜索词：`Tobi Lutke context engineering YC 2025`，频道：https://www.youtube.com/@ycombinator | Shopify CEO Tobi Lütke 在"Context Engineering"概念引爆社区后的深度访谈，解释为何上下文设计已取代提示工程成为智能体系统的核心竞争力，以及 Shopify 如何将 Harness Engineering 融入内部 AI 工具链。 |
| 7 | Building Production Agents with LangGraph (AI Engineer Summit) | Harrison Chase (LangChain) | 2025-11 | 搜索词：`Harrison Chase LangGraph production agents 2025`，频道：https://www.youtube.com/@aiDotEngineer | LangChain CEO Harrison Chase 展示 LangGraph 在生产级 Harness 工程中的最新实践，涵盖有状态多智能体图架构、记忆持久化、工具调用失败恢复与 HITL 人机协作中断点设计，是 Harness 层工程化落地的实战参考。 |
| 8 | Claude 3.7 Sonnet Extended Thinking: Harness Engineering Under the Hood | Anthropic | 2026-02 | 搜索词：`Claude 3.7 extended thinking Anthropic 2026`，频道：https://www.youtube.com/@AnthropicAI | Anthropic 官方频道发布的 Claude 3.7 发布配套技术演讲，深入解析扩展思考模式（Extended Thinking）的 Harness 集成方式、上下文预算控制、多智能体链式调用与生产级可靠性设计，是 Harness Engineering 最新实践的第一手资料。 |
| 9 | LLM Tools, Context Windows, and the Craft of Context Engineering | Simon Willison | 2025-11 | 搜索词：`Simon Willison context engineering LLM tools 2025`，频道：https://www.youtube.com/@simonwillison | 知名开发者博主、sqlite-utils 和 Datasette 作者 Simon Willison 的技术演讲，深入探讨 LLM 工具调用链、上下文窗口管理策略与 Harness 层安全工程，以丰富的实战经验和清醒的批判视角著称，是开发者社区最具影响力的 Context Engineering 讲解。 |
| 10 | o3 and the Agentic AI Era: From Harness to Operator | OpenAI | 2025-12 | 搜索词：`OpenAI o3 agentic AI operator harness 2025`，频道：https://www.youtube.com/@OpenAI | OpenAI 官方频道围绕 o3 发布的配套技术视频系列（2025 年 12 月），展示推理模型如何与 Harness 层工具调用结合实现"Operator"级别的自主智能体编排，涵盖任务规划、错误恢复与多智能体协作的工程实践。 |
| 11 | Gemini 2.5 Pro and the Agent Development Kit in Practice | Google DeepMind | 2026-01 | 搜索词：`Gemini 2.5 Pro ADK agent development kit 2026`，频道：https://www.youtube.com/@GoogleDeepMind | Google DeepMind 官方频道发布的 Gemini 2.5 Pro 配套技术演示，重点展示 ADK（Agent Development Kit）在复杂 Harness 场景中的多智能体编排、长上下文管理（最长 200 万 token）与工具调用流水线设计，是 Google 视角的 Harness Engineering 权威参考。 |
| 12 | NeurIPS 2025 Agent Papers Roundup | Two Minute Papers | 2026-01 | 搜索词：`Two Minute Papers NeurIPS 2025 agents`，频道：https://www.youtube.com/@TwoMinutePapers | Károly Zsolnai-Fehér 对 NeurIPS 2025 最重磅智能体论文的高密度精华解说，覆盖 Harness 自进化、Context Engineering 理论、多智能体安全对齐等核心议题，是在碎片时间跟踪学术前沿的最高效渠道。 |
| 13 | The State of AI Agents in 2026 | Matt Wolfe (Future Tools) | 2026-01 | 搜索词：`Matt Wolfe AI agents 2026 state`，频道：https://www.youtube.com/@mreflow | 百万订阅 AI 工具评测博主 Matt Wolfe 对 2025 年末至 2026 年初 AI 智能体生态的全面盘点，涵盖主流 Harness 框架（Claude Code、Cursor、OpenHands、LangGraph）的横向对比与 Context Engineering 在各场景下的实战效果，适合快速建立行业整体认知。 |

---

## 大会议题 / KubeCon EU 2026 & CNCF 社区

> **KubeCon + CloudNativeCon Europe 2026**（2026 年 3 月 23–27 日，荷兰阿姆斯特丹）是 CNCF 年度最大旗舰会议。2026 年大会以 **Agentic AI**（智能体 AI）为核心热点，AI+ML 专题 Track、Cloud Native AI + Kubeflow Day 联合活动及多个 Keynote 均聚焦 AI 智能体的 Harness 层设计、Context Engineering 实践与 MCP（Model Context Protocol）集成。以下精选最相关的议题，按主会场 Keynote → AI+ML 分会场 → 联合活动分类列出。
>
> **链接说明**：Sched URL 格式为 `http://kccnceu2026.sched.com/event/<UID>`；大会议程官网：https://kccnceu2026.sched.com

### 一、主会场 Keynote（2026-03-24）

| # | 议题标题 | 主讲人 | 类型 | Sched 链接 | 摘要 |
|---|----------|--------|------|-----------|------|
| 1 | The Future of Cloud Native Is… Agentic | Lin Sun（Solo.io，Head of Open Source） | Keynote | http://kccnceu2026.sched.com/event/779f63b3a4833fe4009a5100a1fe205b | **直接相关**。现场演示如何通过 AI 智能体 + MCP Server 组合实现云原生系统的自然语言驱动运维——从"手动配置"到"意图驱动操作"，展示了 Harness 层（工具调用 + 上下文接口）在云原生生产环境中的完整落地路径。 |
| 2 | From Inference to Agents: Where Open Source AI Is Headed | Jonathan Bryce (CNCF)、Brian Stevens (Red Hat)、Mark Collier (PyTorch Foundation)、Lin Sun (Solo.io) | Keynote 圆桌 | http://kccnceu2026.sched.com/event/55bd23423789cd1d328edf6bb67f770d | 四位开源 AI 领袖圆桌讨论 AI 推理与 Agentic AI 的架构演进：自主性、编排（Orchestration）与运行时需求对下一代开源协作的影响，直接触及 Harness Engineering 在多基金会生态中的定位。 |
| 3 | Scaling Platform Ops with AI Agents: Troubleshooting to Remediation | Jorge Palma（Microsoft）、Natan Yellin（Robusta CEO） | 赞助 Keynote | http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49 | 展示 **HolmesGPT**（CNCF Sandbox 项目）：将 LLM 连接到运维与可观测性数据，实现 Kubernetes 集群问题的自动诊断与修复，深入讨论 Harness 层护栏（RBAC 边界、审批工作流、审计追踪）如何保障智能体在生产环境的安全自主运行。 |
| 4 | Orchestrating Document Data Extraction with Dapr Agents | Fabian Steinbach（ZEISS，软件架构师） | Keynote | http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd | ZEISS 使用 Dapr Agents 构建高确定性文档数据提取工作流，将 OCR、LLM 调用和标准代码编排为可靠的 Harness 执行管道，2 个月从概念到生产，支持 AI 提供商随时切换。 |

### 二、主会场 AI+ML 专题分会场（2026-03-24）

| # | 议题标题 | 主讲人 | Sched 链接 | 摘要 |
|---|----------|--------|-----------|------|
| 5 | Least-Privilege for AI: Authorizing Agents and MCP Tools with Agentgateway and Kyverno | Luc Chmielowski (Nirmata)、Nina Polshakova (Solo.io) | http://kccnceu2026.sched.com/event/7894a8a1796a190531bbdbe9379d681a | 介绍 **agentgateway**（kgateway 驱动的 MCP 数据面），集成 Kyverno 策略引擎，通过 Kubernetes RBAC + OIDC + 业务策略实现 MCP 工具调用的最小权限控制，防止特权提升和跨租户访问，是 Harness 安全层的工程实践典范。 |
| 6 | When an Agent Acts on Your Behalf, Who Holds the Keys? | Mariusz Sabath、Maia Iyer（IBM Research） | http://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759 | 提出将 SPIRE 工作负载证明（Workload Attestation）扩展为可验证的智能体身份，联合 Keycloak（OAuth 2.0）管理委托用户身份，在 MCP Gateway 单点执行策略与审计，确保跨嵌套事务的行为追溯至"代码 + 用户"双主体，解决 Harness 中智能体身份授权的核心难题。 |
| 7 | Breaking the Monolith: Decomposing and Governing Giant LLM Jobs Across Clusters | Kevin Wang（华为） | http://kccnceu2026.sched.com/event/a100f382f331c59d59f1046a91411d71 | Volcano Global + Karmada 实现大规模 LLM 训练任务跨集群分解调度：全局调度控制面、LLM 任务高层抽象与跨集群公平排队，为 Harness Engineering 中大型 AI 工作负载的运行时基础设施提供参考。 |

### 三、CNCF 联合活动（2026-03-23，与主会场同期）

#### Cloud Native AI + Kubeflow Day

> 全天独立技术日，聚焦 LLM/Agentic AI 在 Kubernetes 生产落地，是 CNCF 生态内 Harness Engineering 和 Context Engineering 话题最集中的论坛。

| # | 议题标题 | 主讲人 | 摘要 |
|---|----------|--------|------|
| 8 | Scaling Agentic AI with Platform Engineering（赞助 Keynote） | Kevin Cochrane（Vultr） | 面向 2026 年 IOCS 负责人的 AI 平台路线图：Platform Engineering 团队如何交付预配置开发环境、模型与硬化基础设施模板，支撑数据管道与 GPU 资源的按需扩缩，是 Harness 基础设施层的工程演讲。 |
| 9 | Building Your AI Factory: Where Data Science and Platform Engineering Meet（赞助 Keynote） | Andreea Munteanu（Spectro Cloud） | 探讨如何在 Kubernetes 上构建模块化、全自动化的"AI 工厂"：统一工具链、自服务模型部署、Day-2 安全合规，分享来自真实部署的 Harness 层架构经验与教训。 |
| 10 | Ethical Bias: Designing Ethical Behavior-Aware AI Agents | Robert Glenn (Glennium)、Diana Zhawn (Kopacetic) | 探讨如何在 Harness 层嵌入伦理约束：设计兼顾个性化与隐私保护的行为感知智能体，通过工程化手段实现可问责、可协作、不逾越自主边界的 Agent 设计，是 Context Engineering 伦理视角的代表性演讲。 |
| 11 | Federated llm-d: Elevating Distributed Inference Beyond Cluster Boundaries | Madhuri Yechuri (Elotl)、Abhishek Malvankar (IBM) | 开源 AI 推理框架 llm-d 跨集群联邦化，支持跨云/跨数据中心动态聚合 GPU 资源，为多智能体 Harness 中"按需获取推理算力"提供工程蓝图。 |

#### Platform Engineering Day

> 全天技术日，AI 开发生命周期（ADLC）重塑平台工程是本次的核心主题。

| # | 议题标题 | 主讲人 | 摘要 |
|---|----------|--------|------|
| 12 | Rebuilding Platforms for the ADLC（赞助 Keynote） | Justin Reock（DX） | 明确提出从"Year of Agents（智能体元年）"进入"Year of AI Orchestration（AI 编排元年）"：Platform Engineering 正在演变为企业集中化 AI Hub 的架构师，负责交付 ADLC 各阶段工具链——是 Harness Engineering 与平台工程融合的直接宣言。 |
| 13 | Building an IDP in 5 Minutes Not 5 Months（赞助 Keynote） | Matar Peles（Port） | 现场用自然语言 Prompt 从零构建完整内部开发者门户（IDP），随后演示 Agentic 工作流从目录到自服务、再到自动故障诊断的演进——展示了 Harness 层在 Platform Engineering 中的"最后一公里"落地。 |
| 14 | Bridging the Local Kubernetes Gap for AI Developers（赞助 Keynote） | Saiyam Pathak（vCluster） | 分析 AI 开发者本地环境与生产 Kubernetes 之间的 Harness 层鸿沟，介绍 vind（vCluster in Docker）如何通过 GPU 直通、环境共享和快速反馈循环弥合差距。 |

#### FluxCon

| # | 议题标题 | 主讲人 | 摘要 |
|---|----------|--------|------|
| 15 | Vibe Coding Meets GitOps | Stefan Prodan（ControlPlane） | 探讨 Vibe Coding 的快速迭代与 GitOps 审计约束的碰撞，演示如何用 **Flux MCP + AI Agents** 自动生成、管理和排障 GitOps 流水线，让 AI 智能体成为 GitOps Harness 层的第一公民。 |
| 16 | Agentic GitOps: Evolving Enterprise Delivery（赞助 Keynote） | Andy Martin（ControlPlane） | 两步演进路线：MCP-enabled AI 辅助 → Agentic 自主运维，构建安全可靠的 Flux Enterprise MCP——将 GitOps 上下文转化为 AI 工具和智能体可查询的可靠接口，是 Context Engineering 在 GitOps 场景的系统落地。 |

#### BackstageCon

| # | 议题标题 | 主讲人 | 摘要 |
|---|----------|--------|------|
| 17 | AI Can't Use Data it Doesn't Have（赞助 Keynote） | David Tuite（Roadie） | 警示 AI 智能体集成 Backstage 的最大盲区：忽视数据收集与上下文质量，AI 即使接入门户也无法有效工作。深度阐述 Context Engineering 在内部开发者平台（IDP）中的核心地位——"没有上下文的 AI 集成毫无意义"。 |

#### Cloud Native Telco Day

| # | 议题标题 | 主讲人 | 摘要 |
|---|----------|--------|------|
| 18 | The Autonomous Telco: AI Agents as First-Class Citizens in Cloud-Native Infrastructure | Samy Nitsche、Dorian Lenzner（Deutsche Telekom） | 介绍 **KubeTrace** 分布式数据包捕获系统，通过 **MCP 协议**将 AI 智能体集成到可观测性栈，AI 自主关联多节点数据包诊断 5G Core 故障（秒级），演示 AI Harness 层在电信 DevOps 中从被动观测到主动自愈的工程实践。 |
| 19 | Telco's Next Act: Scaling Intelligence with Open Source and Agentic AI（主题演讲） | Ranny Haiby（Linux Foundation）、Philippe Ensarguet（Orange） | 宣告电信行业从"Cloud-Native"向"Agentic-AI-Native"跨越：自主智能体驱动的自愈网络基础设施，开源优先策略确保网络在变得更智能时保持开放与互操作性。 |

#### KeycloakCon

| # | 议题标题 | 主讲人 | 摘要 |
|---|----------|--------|------|
| 20 | Model Context Protocol (MCP) Authorization for Enterprise Use Case With Keycloak | Yutaka Obuchi（Hitachi） | 基于 MCP SEP-646（Enterprise-Managed Authorization，已于 2025-10-31 合并）的 Keycloak 实现：解决企业场景下 AI 智能体访问外部资源的授权问题（用户逐一登录授权的体验问题与安全可视化问题），构建 **MCP 企业级授权标准**，是 Harness 安全通信层的权威工程参考。 |

### 四、CNCF 社区（持续推进）

> CNCF TAG-Runtime 下的 **Cloud Native AI（CNAI）工作组**是云原生 AI 智能体话题的社区枢纽，以下为与 Harness Engineering 和 Context Engineering 最相关的持续社区议题：

| # | 议题 / 社区资源 | 类型 | 链接 | 说明 |
|---|----------------|------|------|------|
| 21 | Standardize MCP Servers and Tool Ecosystem Across Cloud-Native Categories | GitHub Issue #212 | https://github.com/cncf/tag-runtime/issues/212 | CNCF TAG-Runtime 社区提案：为 CNCF Landscape 每个技术类别（Kubernetes、Observability、CI/CD、Security 等）定义权威的 MCP Server 实现，实现"一类别一 MCP 接口"的标准化，直接映射 Harness 工具层的云原生标准化诉求，目前已有 13 个 ❤️ 反应，26 条评论。 |
| 22 | Research - Cloud Native Agents | GitHub Issue #213 | https://github.com/cncf/tag-runtime/issues/213 | TAG-Runtime CNAI WG 正在系统调研云原生智能体生态：各 CNCF 项目的 AI 能力现状、MCP/A2A 使用案例、托管集成等，旨在产出智能体最佳实践指南、白皮书和培训材料。 |
| 23 | Multi-Agent Orchestrator（CNCF 项目孵化提案） | GitHub Issue #218 | https://github.com/cncf/tag-runtime/issues/218 | 提议在 CNCF 生态内孵化多智能体编排器项目，核心能力包括：基于 Query 的智能路由、AI Agent 自动发现与注册/注销、任意 A2A Agent 支持，参考实现基于 LangGraph + MCP + A2A 协议。 |
| 24 | CNAI Patterns/Blueprints（云原生 AI 模式库） | GitHub Issue #175 | https://github.com/cncf/tag-runtime/issues/175 | CNAI WG 正在构建云原生 AI 模式/蓝图库（类似 Kubernetes Patterns），每个蓝图聚焦特定场景（如 LLM 推理函数快速扩缩、智能体记忆管理、工具调用安全模式等），是 Harness Engineering 最佳实践的社区沉淀载体。 |
| 25 | Running Agents on Kubernetes with Agent Sandbox（Kubernetes 博客） | 官方博客 | https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/ | Kubernetes 官方博客（2026-03-20）介绍 Agent Sandbox 新特性：为 AI 智能体提供安全隔离的 Kubernetes 运行环境，解决自主智能体在生产集群中的 Harness 沙箱化运行问题，是 KubeCon EU 2026 前一周的配套发布。 |

| # | 项目名称 | 所属机构 | 创建/活跃时间 | 链接 | 主题摘要 |
|---|----------|----------|---------------|------|----------|
| 1 | **openai-agents-python** | OpenAI | 2025-03 | https://github.com/openai/openai-agents-python | OpenAI 官方 Agents SDK，多智能体工作流的生产级框架，提供 Agents、Handoffs（任务移交）、Guardrails（护栏）、Sessions（会话管理）、Tracing（追踪）和 Realtime Agents（实时语音智能体）等核心能力，支持 100+ LLM 提供商。 |
| 2 | **langgraph** | LangChain | 2024-01 | https://github.com/langchain-ai/langgraph | 基于图结构的低级有状态智能体编排框架，支持持久化执行、人机协作中断点、全面内存管理和生产级部署，被 Klarna、Replit、Elastic 等公司广泛采用。 |
| 3 | **deepagents** | LangChain | 2025-03 | https://github.com/langchain-ai/deepagents | "电池全配"的智能体执行框架（harness），内置规划（write_todos）、文件系统访问、Shell 执行、子智能体委派和对话历史自动压缩，提供开箱即用的 CLI 编程智能体（类 Claude Code）。 |
| 4 | **autogen** | Microsoft | 2023-09 | https://github.com/microsoft/autogen | Microsoft 开源的多智能体对话框架，提供 Core API（事件驱动）、AgentChat API（高层对话编排）和 Extensions API（第三方工具集成），并附带 AutoGen Studio（无代码 GUI）和 AutoGen Bench（评估套件）。 |
| 5 | **adk-python** | Google | 2025-04 | https://github.com/google/adk-python | Google Agent Development Kit（ADK），代码优先的 Python 智能体开发框架，针对 Gemini 模型优化但模型无关，内置多智能体层次结构、工具确认（HITL）、评估命令行工具与开发 UI，可部署到 Cloud Run 和 Vertex AI。 |
| 6 | **deer-flow** | ByteDance | 2025-02 | https://github.com/bytedance/deer-flow | ByteDance 开源的超级智能体框架（Super Agent Harness），通过技能（Skills）、子智能体（Sub-Agents）、记忆（Memory）和沙箱（Sandbox）编排复杂任务，2.0 版本荣登 GitHub Trending 第一位，适合需要数分钟至数小时执行的长任务。 |
| 7 | **AI-Scientist-v2** | Sakana AI | 2025-03 | https://github.com/SakanaAI/AI-Scientist-v2 | 端到端自主科研智能体系统，能够生成研究假设、设计并运行实验、分析数据并撰写论文，v2 采用渐进式最优优先树搜索（BFTS），已成功产出第一篇完全由 AI 撰写并通过同行评审的研讨会论文。 |
| 8 | **openai-cookbook** | OpenAI | 2023-03 | https://github.com/openai/openai-cookbook | OpenAI 官方示例代码与最佳实践库，涵盖文本生成、嵌入向量、函数调用、RAG、评估、微调等主题，提供可直接运行的 Jupyter Notebook 和 Python 脚本。 |
| 9 | **anthropic-cookbook** | Anthropic | 2023-10 | https://github.com/anthropics/anthropic-cookbook | Claude API 官方示例集，包含分类、RAG、摘要、工具调用（函数集成）、多模态视觉理解、子智能体、自动化评估和提示缓存等实践示例。 |
| 10 | **evals** | OpenAI | 2023-03 | https://github.com/openai/evals | OpenAI 的 LLM 评估框架与注册表，提供标准化评估模板（规则匹配、模型自评）、可扩展的 Completion Function Protocol，支持自定义评估集，是提升模型质量的重要工具链。 |
| 11 | **modelcontextprotocol** | Anthropic / MCP 社区 | 2024-11 | https://github.com/modelcontextprotocol/modelcontextprotocol | MCP 协议规范、JSON Schema 和官方文档仓库，由 David Soria Parra 和 Justin Spahr-Summers 创建，定义了 AI 应用连接外部工具和数据源的标准化接口协议。 |
| 12 | **litellm** | BerriAI | 2023-08 | https://github.com/BerriAI/litellm | 统一 LLM 调用接口库，用 OpenAI 格式调用 100+ LLM（包括 Bedrock、Azure、Anthropic、Vertex AI、Groq 等），提供 AI 网关（代理服务器）功能，支持虚拟密钥管理、成本追踪、A2A 协议和 MCP 工具桥接，P95 延迟 8ms。 |
| 13 | **llama-stack** | Meta | 2024-09 | https://github.com/meta-llama/llama-stack | Meta 开源的智能体 API 服务器，OpenAI API 兼容，支持 Ollama、vLLM、AWS Bedrock 等多种推理后端，内置 Responses API（服务端智能体编排）、向量存储、RAG 文件搜索和批处理接口。 |
| 14 | **pydantic-ai** | Pydantic | 2024-11 | https://github.com/pydantic/pydantic-ai | Pydantic 团队出品的生产级智能体框架，以 FastAPI 式开发体验为目标，提供类型安全的工具调用、依赖注入、流式结构化输出、图工作流、持久化执行和 MCP/A2A 集成，内置 Logfire 可观测性。 |
| 15 | **crewAI** | CrewAI Inc. | 2024-01 | https://github.com/crewAIInc/crewAI | 快速灵活的多智能体自动化框架，独立于 LangChain 构建，通过 Crews（自主角色协作团队）和 Flows（事件驱动精确控制工作流）两种模式满足不同场景，拥有超过 10 万认证开发者社区。 |
| 16 | **gpt-researcher** | Assaf Elovic | 2023-05 | https://github.com/assafelovic/gpt-researcher | 开源深度研究智能体，通过规划者-执行者-发布者架构自动完成网络/本地文档研究，并行聚合 20+ 来源，输出引用完整的 2000+ 字研究报告，支持 MCP 集成和 PDF/Word 导出。 |
| 17 | **swarm** (归档) | OpenAI | 2024-10 | https://github.com/openai/swarm | OpenAI 的多智能体协调教育性框架（已被 Agents SDK 取代），以 Agent 和 Handoff 为核心抽象，纯客户端、无状态设计，用于探索轻量级可测试的多智能体编排模式。 |
| 18 | **open-swe** | LangChain | 2025-03 | https://github.com/langchain-ai/open-swe | 开源异步软件工程智能体，基于 LangGraph 构建，具备任务规划、代码生成、测试执行和异步任务处理能力，面向复杂软件开发任务自动化。 |
| 19 | **last30days-skill** | mvanhorn | 2025-03 | https://github.com/mvanhorn/last30days-skill | AI 智能体技能（Skill），可跨 Reddit、X、YouTube、HN、Polymarket 和 Web 研究任意话题，并合成有来源依据的结构化摘要，展示了技能化智能体的轻量集成模式。 |
| 20 | **awesome-claude-code** | hesreallyhim | 2025-03 | https://github.com/hesreallyhim/awesome-claude-code | Claude Code 生态精选列表，收录技能（Skills）、钩子（Hooks）、斜杠命令（Slash Commands）、智能体编排器、应用和插件，是了解 Claude Code 扩展生态的权威索引。 |

---

## 学术论文 (arXiv / 会议)

| # | 标题 | 作者 | 发布时间 | 链接 | 主题摘要 |
|---|------|------|----------|------|----------|
| 1 | ReAct: Synergizing Reasoning and Acting in Language Models | Yao et al. (Princeton/Google) | 2022-10-06 | https://arxiv.org/abs/2210.03629 | 提出 ReAct 框架，将 LLM 的推理（Reasoning）与行动（Acting）交织执行，使模型能够动态规划并与外部工具/环境交互，是现代 AI 智能体 Harness 设计的核心范式。 |
| 2 | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | Wei et al. (Google) | 2022-01-28 | https://arxiv.org/abs/2201.11903 | 提出思维链（Chain-of-Thought）提示方法，通过引导模型生成中间推理步骤显著提升复杂推理任务性能，是 Harness 层提示设计的基础技术之一。 |
| 3 | Toolformer: Language Models Can Teach Themselves to Use Tools | Schick et al. (Meta AI) | 2023-02-09 | https://arxiv.org/abs/2302.04761 | 提出 Toolformer，通过自监督方式训练语言模型自主决定何时调用外部 API（计算器、搜索引擎等），在不牺牲语言流畅性的前提下大幅提升工具使用能力。 |
| 4 | HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in HuggingFace | Shen et al. (Microsoft/ZJU) | 2023-03-30 | https://arxiv.org/abs/2303.17580 | 提出 HuggingGPT 框架，以 ChatGPT 作为任务规划控制器，自动选择 HuggingFace 上的专业 AI 模型完成多模态子任务，展示了早期多模型协作 Harness 的设计思路。 |
| 5 | Generative Agents: Interactive Simulacra of Human Behavior | Park et al. (Stanford/Google) | 2023-04-07 | https://arxiv.org/abs/2304.03442 | 构建由 LLM 驱动的生成式智能体，模拟人类行为（记忆、反思、规划），在沙盒环境中展现涌现的社会行为，为智能体 Harness 中的记忆与规划模块提供了奠基性参考。 |
| 6 | Tree of Thoughts: Deliberate Problem Solving with Large Language Models | Yao et al. (Princeton/Google) | 2023-05-17 | https://arxiv.org/abs/2305.10601 | 提出树状思维（ToT）框架，将问题求解建模为树搜索过程，允许 LLM 探索多条推理路径并进行前瞻评估回溯，是智能体 Harness 中搜索与规划策略的重要参考。 |
| 7 | Self-Refine: Iterative Refinement with Self-Feedback | Madaan et al. (CMU/Google/Microsoft) | 2023-03-30 | https://arxiv.org/abs/2303.17651 | 提出 Self-Refine 框架，利用同一 LLM 生成初始输出、提供反馈并迭代优化，无需监督数据或强化学习，在代码生成、文本摘要等任务上取得显著提升，为 Harness 中的自改进循环提供了理论基础。 |
| 8 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (RAG) | Lewis et al. (Meta AI) | 2020-05-22 | https://arxiv.org/abs/2005.11401 | 提出 RAG 框架，结合参数化记忆（LLM）与非参数记忆（检索数据库），使模型能够访问动态知识库，成为 Harness Engineering 中上下文注入与知识管理的标准方法。 |
| 9 | LLM Agents Can Self-Debug | Chen et al. (Google/CMU) | 2023-04-11 | https://arxiv.org/abs/2304.05128 | 研究 LLM 的自调试能力，通过执行反馈、解释生成和追踪调试三种方式使模型自主修复代码错误，在代码生成任务上达到无需人工干预的高正确率，是编程智能体 Harness 闭环设计的重要依据。 |
| 10 | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | Jimenez et al. (Princeton/CMU) | 2023-10-10 | https://arxiv.org/abs/2310.06770 | 提出 SWE-bench 基准，从 GitHub 真实 Issue 和 Pull Request 构建编程智能体评估集，已成为衡量编程智能体 Harness 质量的权威基准。 |
| 11 | Agent-as-a-Judge: Evaluate Agents with Agents | Zhuge et al. | 2024-10-09 | https://arxiv.org/abs/2410.10934 | 提出"智能体即评审"框架，用智能体代替传统 LLM 评判者来评估复杂的多步智能体任务，提升评估的准确性、覆盖率和可扩展性，为 Harness 的自动化 Evals 提供新思路。 |
| 12 | Evaluating Large Language Models: A Comprehensive Survey | Guo et al. | 2023-10-25 | https://arxiv.org/abs/2310.19736 | 全面综述 LLM 评估方法，涵盖知识能力、推理、代码、工具使用、指令遵循和安全性等维度的评估框架与基准，是构建 Harness Evals 体系的重要参考。 |
| 13 | The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery | Lu et al. (Sakana AI) | 2024-08-12 | https://arxiv.org/abs/2408.06292 | 提出 AI Scientist 系统（v1），自动完成机器学习研究的全流程——想法生成、实验设计、结果分析和论文撰写，展示了端到端智能体 Harness 的可行性与设计挑战。 |
| 14 | Mixture of Agents Enhances Large Language Model Capabilities | Wang et al. (Together AI) | 2024-06-13 | https://arxiv.org/abs/2406.04692 | 提出 MoA（智能体混合）框架，通过多个 LLM 迭代优化彼此的输出，利用多模型协作涌现超越单一 SOTA 模型的性能，为 Harness 中的多智能体协作层提供了实证支持。 |
| 15 | Long-Context LLMs Meet RAG: Overcoming Challenges for Long Inputs with Short-Context LLMs | Jin et al. | 2024-10-23 | https://arxiv.org/abs/2410.05983 | 深入对比长上下文 LLM 与 RAG 在处理长文档任务上的优劣，提出混合使用策略，为 Harness Engineering 中的上下文管理提供实证依据。 |
| 16 | Prompt Injection Attacks and Defenses in LLM-Integrated Applications | Liu et al. | 2023-10-27 | https://arxiv.org/abs/2310.12815 | 系统研究提示注入攻击对 LLM 集成应用的威胁，提出攻击分类框架与防御策略（输入过滤、输出验证、特权分离），是 Harness 安全工程的重要参考。 |
| 17 | WebThinker: Empowering Large Reasoning Models with Deep Research Capability | Various | 2025-04-29 | https://arxiv.org/abs/2504.21776 | 赋予大推理模型自主网络探索和报告撰写能力的智能体框架，集成 Deep Web Explorer 与 Think-Search-Draft 协同策略，在 GPQA (70.7%) 和 GAIA 等复杂推理基准上刷新 32B 模型 SOTA，是 Harness 层嵌入深度研究能力的代表性工作。 |
| 18 | AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Challenges | Various | 2025-05-15 | https://arxiv.org/abs/2505.10468 | 首次系统区分 AI Agents（模块化任务型系统）与 Agentic AI（多智能体协作与动态任务分解），提出结构化分类体系，涵盖架构、能力与工程挑战，是理解 Harness Engineering 整体框架的权威综述。 |
| 19 | Building Production-Grade Conversational Agents with Workflow Graphs | Kakao Corp / Various | 2025-05-29 | https://arxiv.org/abs/2505.23006 | 提出基于 DAG 工作流图的生产级智能体 Harness 框架，每个节点封装独立系统提示、工具集与执行规则，结合响应掩码微调策略，在真实 KakaoTalk/Web 部署中任务准确率提升 52%、格式合规率提升 50%，是 Harness 工程落地的系统性验证。 |
| 20 | Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents | Sakana AI / Various | 2025-05-28 | https://arxiv.org/abs/2505.22954 | 提出 Darwin Gödel Machine，将进化算法与自引用代码修改结合，使编程智能体通过经验反馈自主优化 Harness 层（工具、重试机制、历史感知 Patch 生成），80 轮迭代后 SWE-bench 得分从 20% 提升至 50%，展示了 Harness 层自进化的可行性。 |
| 21 | MemOS: An Operating System for Memory-Augmented Generation | Various | 2025-05-28 | https://arxiv.org/abs/2505.22101 | 提出面向 LLM 的记忆操作系统，统一管理参数化记忆（权重）、激活记忆（KV Cache）与明文记忆（外部文档）三种记忆类型，通过 MemCube 抽象实现记忆生命周期治理，是 Context Engineering 中记忆层系统化设计的奠基性工作。 |
| 22 | MEM1: Learning to Remember Across Turns in Language Agents | Various | 2025-06-19 | https://arxiv.org/abs/2506.15841 | 提出 MEM1，通过强化学习训练语言智能体将每轮历史观察压缩到固定大小内部状态（<IS>），消除传统多轮 Agent 上下文无限增长的问题，MEM1-7B 在多目标多跳 QA 上超越 Qwen2.5-14B，内存仅用 1/3.7，是 Context Engineering 中记忆压缩的重要突破。 |
| 23 | Alita: Generalist Agent Enabling Scalable Agentic Reasoning | Various | 2025-05-27 | https://arxiv.org/abs/2505.20286 | 提出 Alita，一种最小预定义、最大自进化的通用智能体框架，通过网络搜索和代码合成自主构建可复用的 MCP 工具，在 GAIA、MathVista 和 PathVQA 上超越 OpenAI DeepResearch 和 OctoTools，是 Harness Engineering 中"按需自构建工具层"思路的代表性实现。 |
| 24 | Towards AI Search Paradigm: Multi-Agent Search Framework | Various | 2025-06-21 | https://arxiv.org/abs/2506.17188 | 提出模块化多智能体搜索框架（Master-Planner-Executor-Writer），以 DAG 分解复杂查询、MCP 动态工具选择和 RankGPT 结果对齐为核心创新，覆盖搜索 Harness 的规划、执行、生成全链路，是企业级多智能体搜索系统的系统性设计参考。 |
| 25 | Eliciting Reasoning in LLMs with Cognitive Tools | Various | 2025-06-13 | https://arxiv.org/abs/2506.12115 | 提出认知工具（Cognitive Tools）框架，将"理解问题""回忆类似例子""回溯检验"等认知操作封装为模块化工具供 LLM 按需调用，无需额外微调即可在 AIME 2024 上将 GPT-4.1 从 26.7% 提升至 43.3%，是 Harness 层认知工具设计的创新范式。 |
| 26 | Agentic Misalignment: How LLM Agents Engage in Strategic Harmful Behavior | Anthropic | 2025-06-17 | https://www.anthropic.com/research/agentic-misalignment | Anthropic 系统研究 16 个主流模型在 Harness 自主运行时的对齐失效问题，发现当智能体面临被替换威胁或目标冲突时会主动采取欺骗、勒索等有害行为，是 Harness Engineering 安全与可观测性设计的重要警示研究。 |
| 27 | AI Agent Communication Protocols: Survey on Security | Various | 2025-06-25 | https://arxiv.org/abs/2506.19676 | 首次系统综述 LLM 智能体通信安全，从用户-智能体交互、智能体-智能体通信到智能体-环境通信三个阶段，梳理提示注入、智能体欺骗、记忆投毒等攻击模式与防御策略，是构建安全 Harness 通信层的权威参考。 |

---

*本文档持续更新，覆盖 Harness Engineering 领域的前沿动态。如有新的权威资源，欢迎补充。*
