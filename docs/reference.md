# Harness Engineering 参考资源清单

> 聚焦 Harness Engineering 核心主题：围绕 AI 编程智能体的脚手架与工具层（Scaffolding/Harness）、上下文工程（Context Engineering）、技能与工具集成（Skills & Tools）、智能体框架与编排（Agent Orchestration）、评估与测试（Evals）等。收集来源：OpenAI、Anthropic、Martin Fowler/Thoughtworks、LangChain、HumanLayer 及主流 arXiv 论文。
>
> 最后更新：2026-03-28

---

## 目录

- [博客文章 / 行业报告](#博客文章--行业报告)
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

## GitHub 开源项目

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

---

*本文档持续更新，覆盖 Harness Engineering 领域的前沿动态。如有新的权威资源，欢迎补充。*
