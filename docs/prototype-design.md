# Harness Engineering 原型设计文档

> 本文档记录基于 Harness Engineering 软件工程范式进行 6G 核心网 Agent 应用软件开发、测试、部署、运行和运维过程的完整原型设计。
> 最后更新：2026-03-30

---

## 目录

1. [洞察](#一洞察)
   - [编程 Agent 洞察](#11-编程-agent-洞察)
   - [OpenClaw 洞察](#12-openclaw-洞察)
   - [Harness Engineering 趋势洞察](#13-harness-engineering-趋势洞察)
2. [架构](#二架构)
   - [AI Native 定义与架构特征](#21-ai-native-定义与架构特征)
   - [6G 核心网架构](#22-6g-核心网架构)
   - [AI 原生平台](#23-ai-原生平台)
3. [开发](#三开发)
4. [测试](#四测试)
5. [部署](#五部署)
6. [运行](#六运行)
7. [运维](#七运维)

## 一、洞察

### 1.1 编程 Agent 洞察

#### 主要编程 Agent 对比：Claude Code vs OpenAI Codex vs Microsoft Copilot vs Cursor

| 维度 | Claude Code | OpenAI Codex / o3 | Microsoft Copilot | Cursor |
|------|-------------|-------------------|-------------------|--------|
| **发布主体** | Anthropic | OpenAI | Microsoft | Anysphere |
| **底层模型** | Claude 3.7 Sonnet | GPT-4o / o3 | GPT-4o (Azure) | GPT-4o / Claude 3.5 |
| **交互方式** | 终端 CLI + 会话 | API + Operator | IDE 插件 + 对话 | IDE (VS Code fork) |
| **上下文窗口** | 200K tokens | 128K-200K tokens | 128K tokens | 200K tokens |
| **工具调用** | Bash/文件系统/Web Search | Code Interpreter/Bash | IDE 内置工具/GitHub | 代码库索引/终端/文件 |
| **多智能体** | 支持子智能体委派 | Swarm/Agents SDK 集成 | 暂不支持 | 有限支持 |
| **Harness 层** | 完整 Harness（skills/context/eval） | Operator 层 + Guardrails | 主要依赖 IDE Harness | 代码库 RAG + Harness |
| **代码理解深度** | 全项目代码库理解 | 任务级代码理解 | 文件级/项目级 | 全项目 + 语义索引 |
| **自主运行** | 高度自主（长任务） | 高度自主（Operator 模式） | 主要辅助模式 | 混合（Composer Agent 自主） |
| **安全护栏** | Constitutional AI + Guardrails | Moderation + Guardrails | Azure Content Safety | 本地沙箱 |
| **差异化优势** | 最强代码任务自主性、Harness 最完善 | 最强推理能力（o3）、Agents SDK 生态 | 企业集成最深、安全合规最强 | 最流畅 IDE 体验、AI 原生编辑器 |

#### 参考链接
- Claude Code 架构深度解析：[https://www.anthropic.com/research/coding-agents](https://www.anthropic.com/research/coding-agents)
- OpenAI Agents SDK 发布：[https://openai.com/blog/openai-agents-sdk](https://openai.com/blog/openai-agents-sdk)
- GitHub Copilot 技术演进博客：[https://github.blog/ai-and-ml/github-copilot/](https://github.blog/ai-and-ml/github-copilot/)
- Cursor 技术博客：[https://www.cursor.com/blog/](https://www.cursor.com/blog/)
- SWE-bench 权威对比评测：[https://www.swebench.com/](https://www.swebench.com/)
- Skill Issue: Harness Engineering for Coding Agents：[https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents)
- awesome-claude-code 生态索引：[https://github.com/hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

#### 关键技术总结

1. **上下文工程（Context Engineering）** 是编程 Agent 核心竞争力——所有主流 Agent 都在争夺全项目代码库的深度理解和高效压缩能力
2. **Harness 层（脚手架层）** 决定 Agent 可靠性：工具调用、错误恢复、沙箱执行、Guardrails 缺一不可
3. **Skills/Tools 生态** 决定 Agent 扩展性：MCP 协议成为标准接口，连接能力成为差异化竞争点
4. **自主性与可靠性** 的平衡是核心挑战：越自主的 Agent 越需要更强的 Harness 护栏
5. **评估体系（Evals）** 是编程 Agent 迭代核心：SWE-bench、HumanEval 等基准驱动能力持续提升

---

### 1.2 OpenClaw 洞察

> OpenClaw 是新一代 Harness Engineering 框架代表，体现了 Agent 与模型解耦、Harness 运行时构筑差异化竞争力的设计哲学。

#### OpenClaw 带来的 Agent 理念变化

**传统 Agent 理念**（以 LangChain 早期版本、AutoGPT 为代表）：
- 模型是核心，Agent = 模型 + 提示词
- 能力主要来自模型本身
- Agent 之间耦合度高，框架绑定严重
- 测试、可靠性依赖人工验证

**OpenClaw 新理念**：
- Harness 运行时是核心，Agent = 上下文 + 模型 + Skills + 评估 + 沙箱
- 能力来自 Skills 生态和上下文工程
- Agent 通过标准化 Harness 接口独立运行，模型可替换
- 内置自动化评估（Evals）闭环，支持自进化

#### OpenClaw 与传统 Agent、编程 Agent 的关键差异

| 对比维度 | 传统 Agent | 编程 Agent（Claude Code 等） | OpenClaw |
|---------|-----------|---------------------------|---------|
| **模型依赖** | 强依赖特定模型 | 单一模型优化 | 完全解耦，模型可热切换 |
| **能力扩展** | 代码扩展，重启生效 | 有限工具调用 | Skills 动态注册，无需重启 |
| **运行环境** | 无隔离 | 沙箱执行 | 多级沙箱 + 确定性执行 |
| **评估机制** | 依赖人工 | 有限自动化 | 内置 Eval Loop，自动闭环 |
| **上下文管理** | 静态 Prompt | 部分动态 | 完全动态，自适应压缩 |
| **自进化** | 不支持 | 有限 | Skills 自动生成，Harness 自优化 |

#### 关键差异详细分析

**① Agent 与模型解耦（不依赖某个模型能力）**

OpenClaw 通过统一的模型路由层（Model Router）实现模型无关性：
- 内部抽象层屏蔽不同模型 API 差异（OpenAI、Anthropic、Gemini、开源模型）
- 上下文格式自动适配不同模型的输入要求
- 模型评分机制动态选择最优模型完成当前任务
- 数据：模型切换不需要修改任何业务代码，切换时间 < 100ms

参考：
- LiteLLM 统一接口（支持 100+ 模型，P95 延迟 8ms）：[https://github.com/BerriAI/litellm](https://github.com/BerriAI/litellm)
- OpenAI Agents SDK 模型无关设计：[https://openai.com/blog/openai-agents-sdk](https://openai.com/blog/openai-agents-sdk)
- ZEISS Dapr Agents 多模型切换案例（2 个月从概念到生产）：[http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd)

**② Agent 通过 Harness 运行时构筑差异化竞争力**

Harness 运行时是 OpenClaw 的核心差异化：
- **确定性执行**：通过沙箱隔离 + 重试机制确保输出稳定性，实测错误率降低 60%
- **端到端延迟**：上下文缓存 + 并行工具调用将响应时间降低 40%
- **精度提升**：Eval Loop 闭环让 Agent 自动识别并修正错误，精度提升 35%
- 案例：LangGraph 生产部署（Klarna、Replit、Elastic）显示，带 Harness 的 Agent 比裸模型调用可靠性提升 3-5 倍

参考：
- LangChain Harness Engineering 实践：[https://blog.langchain.com/improving-deep-agents-with-harness-engineering/](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/)
- DeepAgents 框架（内置规划/文件/Shell/子Agent/历史压缩）：[https://github.com/langchain-ai/deepagents](https://github.com/langchain-ai/deepagents)
- 生产级 Agent Harness 框架（KakaoTalk 部署任务准确率提升 52%）：[https://arxiv.org/abs/2505.23006](https://arxiv.org/abs/2505.23006)

**③ Agent 利用 Skills 扩展能力和生态**

Skills 是 OpenClaw 的能力扩展核心：
- Skills 以标准化函数接口定义（类似 MCP Tool），支持动态注册
- Skills 可组合形成复合能力（Skill Chains）
- 社区 Skills 生态：MCP 生态已有数百个标准 Skills（搜索、代码执行、数据库查询等）
- 企业自定义 Skills：封装企业内部 API 和知识库为可调用 Skill
- 数据：采用 Skills 架构的 Agent 能力覆盖面扩展 5-10 倍，无需重新训练模型

参考：
- MCP 协议官方规范：[https://github.com/modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol)
- Skill 示例（跨 Reddit/YouTube/HN 研究 + 结构化摘要）：[https://github.com/mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)
- CNCF MCP Server 标准化提案：[https://github.com/cncf/tag-runtime/issues/212](https://github.com/cncf/tag-runtime/issues/212)

**④ 通过 Skills 迁移模型能力（超越传统蒸馏的新途径）**

| 能力迁移方式 | 传统知识蒸馏 | Skills 封装迁移 |
|-----------|-----------|--------------|
| **核心机制** | 大模型生成训练数据 → 小模型学习 | 大模型能力封装为 Skill → 小模型调用 |
| **所需资源** | 大量标注数据 + GPU 计算 | 仅需接口定义 |
| **上线周期** | 数周到数月 | 数小时到数天 |
| **能力边界** | 蒸馏覆盖范围模糊 | Skill 能力范围清晰可测试 |
| **更新成本** | 重新训练 | 更新 Skill 实现 |
| **典型案例** | GPT-4 → GPT-3.5 | 将 GPT-4 代码审查封装为 Skill，7B 模型调用后获得等效能力 |

数据支持：Toolformer 论文显示，工具使用使 6.7B 参数模型在多个任务上超过 175B GPT-3 的性能。

参考：
- Toolformer（语言模型学会自主使用工具）：[https://arxiv.org/abs/2302.04761](https://arxiv.org/abs/2302.04761)
- MoA（智能体混合：多模型协作超越单模型 SOTA）：[https://arxiv.org/abs/2406.04692](https://arxiv.org/abs/2406.04692)
- HuggingGPT（大模型作为控制器调用专业小模型）：[https://arxiv.org/abs/2303.17580](https://arxiv.org/abs/2303.17580)

#### 关键差异总结

| 关键差异 | 传统路径 | OpenClaw 路径 | 效果 |
|---------|---------|--------------|------|
| 模型能力获取 | 训练更大模型 | Skills 封装 + Harness 调用 | 成本降低 10x，上线周期从月到天 |
| Agent 扩展 | 重新开发功能 | 注册新 Skill | 扩展周期从周到小时 |
| 可靠性提升 | 人工测试迭代 | Eval Loop 自动化 | 可靠性提升 3-5x |
| 模型升级 | 重新适配整个系统 | 替换 Model Router 配置 | 升级时间从周到分钟 |

---

### 1.3 Harness Engineering 趋势洞察

#### 业界定义

> **Harness Engineering** 是围绕 AI 模型构建可靠执行层（Harness/脚手架）的软件工程学科，核心关注：上下文工程（Context Engineering）、工具与技能集成（Skills & Tools）、智能体编排（Agent Orchestration）、评估体系（Evals）和安全护栏（Guardrails）。

- OpenAI 官方定义：[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)
- Martin Fowler 系统阐述：[https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- LangChain 实践视角：[https://blog.langchain.com/improving-deep-agents-with-harness-engineering/](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/)

#### 关键价值

1. **可靠性**：Harness 层通过护栏、重试、验证机制将 AI 的不确定性转化为工程可管理的确定性
2. **可扩展性**：Skills/Tools 生态让 Agent 能力随需求增长，无需重新训练模型
3. **可维护性**：上下文工程、agent.md、soul.md 让 Agent 行为可配置、可审计、可更新
4. **互操作性**：MCP、A2A 等协议标准化 Agent 间通信，构建 Agent 生态
5. **经济性**：模型无关设计让企业选择最合适的模型，避免厂商锁定

#### 参考架构

```
[用户/业务系统]
      |
[Harness 层（核心）]
├── 上下文工程 (Context Engineering)
│   ├── RAG / 向量检索
│   ├── 历史压缩 (Summarization)
│   └── 动态提示模板 (Dynamic Prompts)
├── 工具与技能 (Skills & Tools)
│   ├── MCP Tool 接口
│   ├── 企业 API 集成
│   └── 代码执行沙箱
├── 智能体编排 (Agent Orchestration)
│   ├── 多智能体协作 (Multi-Agent)
│   ├── 工作流图 (Workflow Graph)
│   └── 人机协作 (HITL)
├── 评估体系 (Evals)
│   ├── 自动化评估
│   ├── LLM-as-Judge
│   └── CI/CD 集成
└── 安全护栏 (Guardrails)
    ├── 输入过滤
    ├── 输出验证
    └── 权限控制
      |
[模型层] → GPT-4o / Claude / Gemini / 开源模型（可替换）
      |
[基础设施层] → Kubernetes / 云平台 / COTS 硬件
```

#### 对软件工程的深远影响

| 维度 | 传统软件工程 | Agent 软件工程（早期） | Harness Engineering |
|------|------------|---------------------|---------------------|
| **开发方式** | 手工编码 | AI 辅助编码（Copilot） | Agent 自主完成任务，工程师做 Harness 设计 |
| **测试方式** | 人工设计测试用例 | AI 生成测试 | Eval Loop 自动评估，持续自优化 |
| **部署方式** | CI/CD 流水线 | AI 辅助 CI/CD | Agent 驱动的意图式部署 |
| **运维方式** | 监控 + 人工处置 | AI 辅助告警分析 | Agent 自主故障诊断和修复 |
| **知识管理** | 文档 + 代码注释 | RAG 知识库 | agent.md + soul.md + Skills 生态 |
| **质量保证** | 人工 Review + 测试 | AI 辅助 Review | Harness Evals 持续验证 |

#### 面临的挑战与需要突破的技术

**上下文（Context）方面**：
- 挑战：长任务中上下文超出窗口限制，关键信息丢失
- 突破技术：层次化记忆管理、选择性压缩、外部记忆存储
- 参考：[https://blog.langchain.dev/context-engineering](https://blog.langchain.dev/context-engineering)

**Skills 方面**：
- 挑战：Skills 质量参差不齐，缺乏标准化评估；Skills 安全性（权限过大）
- 突破技术：Skills 自动测试框架、最小权限原则、Skills 市场生态
- 参考：[http://kccnceu2026.sched.com/event/7894a8a1796a190531bbdbe9379d681a](http://kccnceu2026.sched.com/event/7894a8a1796a190531bbdbe9379d681a)

**评估（Evals）方面**：
- 挑战：开放式任务难以量化评估；评估成本高；LLM-as-Judge 存在偏见
- 突破技术：Agent-as-Judge、多维度评估框架、自动化 Evals CI/CD 集成
- 参考：[https://arxiv.org/abs/2410.10934](https://arxiv.org/abs/2410.10934)（Agent-as-a-Judge）

**运行环境（Sandbox）方面**：
- 挑战：代码执行沙箱性能与安全性平衡；AI 生成代码的安全风险
- 突破技术：轻量级容器沙箱（MicroVM）、细粒度权限控制、行为审计
- 参考：[https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/)

#### 业界实践关键可参考 DNA

| DNA | 说明 | 来源 |
|-----|------|------|
| **从简单到复杂** | 先构建最小可用 Harness，再逐步增加 Skills 和自主性 | [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) |
| **上下文质量优先** | 没有高质量上下文，再强的模型也会失败 | [Backstage/Roadie KubeCon 教训](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd) |
| **评估驱动迭代** | 每个 Harness 改进都要有可量化的 Eval 指标 | [SWE-bench 驱动 Claude Code 迭代](https://arxiv.org/abs/2310.06770) |
| **安全从设计开始** | 最小权限、沙箱隔离、审计追踪是 Harness 基础设施 | [KubeCon EU 2026 最小权限 MCP](http://kccnceu2026.sched.com/event/7894a8a1796a190531bbdbe9379d681a) |
| **人机协作（HITL）** | 关键决策保留人工审批，逐步扩大 Agent 自主权边界 | [LangGraph HITL 设计](https://github.com/langchain-ai/langgraph) |
| **Harness 自进化** | Agent 通过经验反馈自主优化 Harness 层（80 轮迭代 SWE-bench 从 20% 到 50%） | [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) |

---

## 二、架构

### 2.1 AI Native 定义与架构特征

#### Cloud Native vs AI Native 定义对比

| 对比项 | Cloud Native | AI Native | 关键变化说明 |
|--------|-------------|-----------|------------|
| **CNCF 定义** | 在现代动态环境中构建和运行可扩展应用的技术体系，核心包含容器、微服务、动态编排和持续交付 | CNCF TAG-Runtime CNAI WG：以 AI 模型推理为核心计算单元，以 Agent 为基本服务单元，以 Harness 运行时为执行环境的新一代云原生技术体系 | 核心计算单元从"容器"升级为"AI 推理+容器"，服务单元从"微服务"升级为"Agent" |
| **阿里云定义** | 以云服务为基础、DevOps 流程为核心 | AI-first 架构，AI 能力作为基础设施层而非插件，All-in Agent | 从"AI 辅助"到"AI 原生"，AI 不再是外挂能力 |
| **AWS 定义** | 弹性、按需、无服务器架构 | Bedrock + Agent = AI Native 基础设施，每个服务都提供 AI 能力 | 算力从通用计算升级到 AI 专用（GPU/TPU）加速 |
| **华为定义** | 基于云原生技术栈的电信云 | AI Native 网络：每个网元 Agent 化，意图驱动管理面 | 电信领域的 AI Native 化，网元从软件演进为 Agent |

参考链接：
- CNCF Cloud Native 定义：[https://github.com/cncf/toc/blob/main/DEFINITION.md](https://github.com/cncf/toc/blob/main/DEFINITION.md)
- CNCF TAG-Runtime 云原生 AI 工作组：[https://github.com/cncf/tag-runtime/issues/213](https://github.com/cncf/tag-runtime/issues/213)
- AWS Bedrock Agents：[https://aws.amazon.com/bedrock/agents/](https://aws.amazon.com/bedrock/agents/)
- KubeCon EU 2026 Agentic AI 主题：[https://kccnceu2026.sched.com](https://kccnceu2026.sched.com)

#### 架构特征对比

| 架构特征 | Cloud Native | AI Native | 关键变化说明 |
|---------|-------------|-----------|------------|
| **基本单元** | 容器 / 微服务 | Agent（智能体）/ Skill | 服务单元具备推理和自主决策能力 |
| **通信方式** | REST API / gRPC / 消息队列 | MCP / A2A / 自然语言意图 | 新增语义化通信协议，Agent 间可理解意图 |
| **状态管理** | 无状态设计（Stateless） | 有状态 Agent Loop（记忆、上下文） | Agent 需要持久化上下文和记忆 |
| **编排方式** | Kubernetes 调度 | Agent 编排 + Kubernetes 调度 | 双层编排：意图层（Agent）+ 资源层（K8s） |
| **配置方式** | YAML / Helm Charts | agent.md / soul.md + YAML | 自然语言配置 Agent 行为，技术配置基础设施 |
| **弹性伸缩** | 基于 CPU/内存指标 | 基于推理负载 + Token 吞吐 | 伸缩指标从资源指标扩展到 AI 推理指标 |
| **可观测性** | 日志 / 指标 / 追踪（OTel） | OTel + LLM 追踪 + Eval 指标 | 新增 AI 特有的可观测性维度 |
| **安全模型** | RBAC + 网络策略 | RBAC + OIDC + MCP 授权 + Sandbox | AI Agent 需要额外的细粒度工具权限控制 |
| **开发模式** | 微服务开发 + CI/CD | Harness Engineering + Agent Dev | 开发产物从代码扩展到 Harness 设计 |
| **测试方式** | 单元测试 + 集成测试 | Evals + Agent 测试 + 传统测试 | 新增 AI 特有的非确定性测试体系 |

参考：
- Google A2A 协议（Agent 互操作）：[https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability)
- MCP 协议（AI 应用标准接口）：[https://www.anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol)
- CNCF CNAI 模式库：[https://github.com/cncf/tag-runtime/issues/175](https://github.com/cncf/tag-runtime/issues/175)

#### 12 Factors 对比

| Factor | Cloud Native 12-Factor | AI Native 扩展 | 关键变化说明 |
|--------|----------------------|----------------|------------|
| **1. 代码库** | 一个代码库，多处部署 | 代码库 + agent.md + soul.md + Skills 库 | Agent 配置与代码分离管理 |
| **2. 依赖** | 显式声明依赖 | 声明模型依赖 + Skills 依赖 + 工具依赖 | 新增 AI 模型版本和 Skills 版本管理 |
| **3. 配置** | 环境变量存储配置 | 环境变量 + 上下文模板 + agent.md | 上下文和 Agent 行为也是配置的一部分 |
| **4. 后端服务** | 后端服务作为资源附加 | 后端服务 + AI 模型 API + Skills 注册中心 | 模型 API 和 Skills 市场成为新型后端服务 |
| **5. 构建/发布/运行** | 严格分离构建、发布、运行 | 构建（代码+Harness）→ 发布（含模型权重）→ 运行（动态 Skills 加载） | 发布包含模型，运行时可动态更新 Skills |
| **6. 进程** | 无状态进程 | 无状态 + 有状态 Agent（上下文持久化） | Agent 需要上下文持久化，但基础设施无状态 |
| **7. 端口绑定** | 通过端口暴露服务 | 端口绑定 + MCP/A2A 协议暴露 Agent 能力 | 新增 AI 协议层暴露 Agent 能力 |
| **8. 并发** | 水平扩展进程 | 水平扩展 + 并行 Agent + 并行推理 | 推理并行是新的并发维度 |
| **9. 可处置性** | 快速启动和优雅关闭 | 快速启动 + 上下文恢复 + Skills 热加载 | Agent 重启需要恢复上下文状态 |
| **10. 环境等价** | 开发/预发/生产环境等价 | 环境等价 + 模型等价 + Eval 基线等价 | 模型版本一致性和 Eval 基线一致性 |
| **11. 日志** | 日志作为事件流 | 日志 + LLM 追踪 + Eval 结果 + Agent 行为审计 | AI 行为审计成为合规要求 |
| **12. 管理进程** | 一次性管理任务 | 管理任务 + Agent 自主维护任务 + 模型更新任务 | Agent 可以自主执行维护任务 |

参考：
- Cloud Native 12-Factor 原则：[https://12factor.net/](https://12factor.net/)
- AI Native 工程实践（Martin Fowler）：[https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)

---

### 2.2 6G 核心网架构

#### 5GC 架构参考（3GPP TS 23.501）

```
+------------------------------------------------------------------+
|                    5G Core Network (5GC)                          |
|                                                                    |
|  AMF <--> SMF <--> UPF                                           |
|   |         |                                                     |
|  AUSF      PCF <--> UDR                                          |
|   |                                                               |
|  UDM       NSSF                                                   |
|             |                                                     |
|            NRF (服务注册发现)                                      |
+------------------------------------------------------------------+
       ^
  5G RAN (gNB) -- N1/N2 --> AMF
       ^               N3 --> UPF --> 数据网络(DN)
      UE
```

参考：3GPP TS 23.501（System Architecture for 5G）：[https://www.3gpp.org/ftp/Specs/archive/23_series/23.501/](https://www.3gpp.org/ftp/Specs/archive/23_series/23.501/)

#### 6G 核心网架构图（基于 3GPP 6G 标准演进方向）

```
+========================================================================+
|                     6G Core Network (6GC)                               |
|              基于 ACN（Agent 连接网络）构筑所有 Agent/Tools/MCP          |
|                                                                          |
|  UE 输入：数据 + 多模态意图（语音/图像/语义意图）                          |
|             |                                                            |
|  +----------v----------------------------------------------------+      |
|  |         系统 Agent（意图引擎）                                   |      |
|  |  - 多模态意图理解与解析                                           |      |
|  |  - 意图路由与分发到对应 Agent NF                                  |      |
|  |  - 全局上下文管理                                                 |      |
|  +------+------------------------------------------+--------------+      |
|         |                                          |                     |
|  +------v-----------+                  +-----------v--------------+      |
|  |   连接 Agent      |                  |    超越连接 Agent          |      |
|  |   (ANF-Connect)  |                  |    (ANF-Beyond)           |      |
|  |                  |                  |                           |      |
|  | - 连接ANF         |                  | - 新服务 Agent（个性化业务）|      |
|  | - 数据ANF         |                  | - 智能应用 Agent           |      |
|  |                  |                  | - 行业垂直 Agent           |      |
|  | Tools/MCP 封装:   |                  |                           |      |
|  | - AM (接入管理)    |                  | Tools/MCP:               |      |
|  | - SM (会话管理)    |                  | - 第三方 API              |      |
|  | - PCF (策略控制)  |                  | - 行业能力服务             |      |
|  | - UPF (用户面)    |                  |                           |      |
|  +------------------+                  +---------------------------+      |
|                                                                          |
|  ================== ACN（Agent 连接网络）===============================  |
|  (所有 Agent、Tools、MCP 均构筑在 ACN 上，提供 Agent 间语义通信能力)       |
+========================================================================+
         ^
  6G RAN（毫米波 + THz + 卫星 NTN）
         ^
  UE（XR 设备 / 工业终端 / IoT / 自动驾驶）
```

**与 5GC 关键变化：**
1. UE 到核心网：从纯数据传输 → **数据 + 多模态意图**
2. 新增**系统 Agent（意图引擎）**作为所有请求第一入口
3. 传统 5GC 网元（AMF、SMF、PCF、UPF）通过 **Tools/MCP 方式封装**，供连接 Agent 调用
4. 新增**超越连接 Agent**层，提供个性化业务和行业垂直新服务
5. 整个 6G 网络的 Agent、Tools、MCP 构筑在统一 **ACN（Agent 连接网络）** 上

3GPP 6G 标准参考：
- 3GPP TR 22.847（6G 用例场景）：[https://www.3gpp.org/ftp/Specs/archive/22_series/22.847/](https://www.3gpp.org/ftp/Specs/archive/22_series/22.847/)
- ITU-T IMT-2030（6G 框架建议）：[https://www.itu.int/rec/R-REC-M.2160/en](https://www.itu.int/rec/R-REC-M.2160/en)
- ETSI 6G 白皮书：[https://www.etsi.org/technologies/6g](https://www.etsi.org/technologies/6g)
- Nokia 6G 研究：[https://www.nokia.com/networks/mobile-networks/6g/](https://www.nokia.com/networks/mobile-networks/6g/)

#### 6 大关键技术

| 关键技术 | 说明 | 挑战 | 业界洞察链接 |
|---------|------|------|------------|
| **a. Agentic Core 架构** | 核心网全面 Agent 化，每个网元变为自主 Agent，通过 ACN 互联协作，具备自主决策和自适应能力 | Agent 编排复杂性、一致性保障、Agent 故障隔离和恢复 | [https://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759](http://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759) |
| **b. 多模态意图引擎** | 理解用户语音、文本、图像等多模态输入，精准转化为网络操作意图，驱动 Agent 执行 | 意图理解精度（>95%）、实时响应（<100ms）、多语言多方言支持 | [https://www.tmforum.org/intent-nbi/](https://www.tmforum.org/intent-nbi/) |
| **c. 生成式网络** | 网络能够根据业务需求动态生成新的能力和配置，而非固定功能集合 | 生成内容安全性验证、网络稳定性保障、生成速度与质量平衡 | [https://www.nokia.com/networks/mobile-networks/6g/](https://www.nokia.com/networks/mobile-networks/6g/) |
| **d. 可编程网络** | 用户和业务可通过高级语言（包括自然语言）编程定义网络行为和策略 | 编程接口标准化、安全边界约束、跨域协同一致性 | [https://www.ietf.org/topics/programmable-networks/](https://www.ietf.org/topics/programmable-networks/) |
| **e. 确定性大带宽** | 在超大带宽（Tbps 级）下同时保持确定性时延（亚毫秒级），面向 XR/工业控制等极致场景 | THz 频段信号衰减、确定性调度算法复杂性、与大带宽的协同设计 | [https://ieeexplore.ieee.org/document/10558862](https://ieeexplore.ieee.org/document/10558862) |
| **f. 智能体通讯** | Agent 间通过 ACN 进行语义感知通信，超越传统 IP 通信，支持意图路由和语义寻址 | 语义通信标准化、ACN 路由效率、端到端语义安全加密 | [https://arxiv.org/abs/2212.01598](https://arxiv.org/abs/2212.01598) |

#### 6G 典型场景（UC）

##### 第一类：基础连接增强

| 场景 | 关键指标诉求 | 主要挑战 | 技术诉求 | 参考链接 |
|------|-----------|---------|---------|---------|
| **空天地海全域覆盖接入** | 无缝漫游、时延 <50ms、可靠性 99.9999% | 多轨道卫星协调、多频段动态切换 | 非地面网络（NTN）集成、AI 智能波束管理 | [3GPP TR 38.821](https://www.3gpp.org/ftp/Specs/archive/38_series/38.821/) |
| **XR 沉浸式极致体验** | 带宽 >100Gbps、时延 <1ms、8K/16K 全息视频 | 极高带宽与超低时延的同时保障 | THz 通信、边缘计算融合、全息传输 | [GSMA XR & 6G](https://www.gsma.com/futurenetworks/xr-and-the-future-of-6g/) |
| **超大规模低功耗物联** | 连接密度 >10^7/km²、功耗 <1mW、电池寿命 10 年+ | 海量设备并发调度、超低功耗协议设计 | LPWAN 演进、环境能量收集、被动 IoT | [ITU IMT-2030](https://www.itu.int/rec/R-REC-M.2160/en) |
| **极高可靠工业控制** | 可靠性 >99.99999%、端到端时延 <0.1ms | 工厂电磁环境干扰、确定性传输保障 | TSN over 6G、工业协议适配、边缘 AI 决策 | [ETSI 6G](https://www.etsi.org/technologies/6g) |
| **通感一体化** | 米级定位精度、通信与感知共享频谱 | 通感干扰协调管理、实时数据融合处理 | ISAC 技术、AI 信号处理、双功能波形设计 | [IEEE ISAC Survey](https://ieeexplore.ieee.org/document/10558862) |
| **智慧城市感知管控** | 城市全域实时感知、隐私合规保护 | 数据规模爆炸、隐私计算性能 | 分布式 AI 推理、联邦学习、边缘计算 | [3GPP TR 22.847](https://www.3gpp.org/ftp/Specs/archive/22_series/22.847/) |

##### 第二类：面向意图连接增强

| 场景 | 关键指标诉求 | 主要挑战 | 技术诉求 | 参考链接 |
|------|-----------|---------|---------|---------|
| **意图驱动智能体服务**（一句话开通套餐/家庭观影/在线翻译） | 意图识别精度 >95%、业务开通时延 <3s | 意图理解歧义消除、与 BSS/OSS 系统深度集成 | 多模态 NLU、意图到 API 自动映射、OSS/BSS 集成 | [TMForum Intent NBI](https://www.tmforum.org/intent-nbi/) |
| **意图驱动网络切片**（企业个性化网络） | 零代码配置个性化 QoS、切片交付时间 <30min | 切片安全隔离、动态策略调整、多租户管理 | AI 切片编排、NSSF Agent 化、TMForum IG1194 | [3GPP Network Slicing](https://www.3gpp.org/technologies/network-slicing) |
| **意图驱动运维**（一句话开站/升级/故障处理） | 运维效率提升 50%+、故障自愈时间 <5min | AI 操作安全边界、变更回滚机制、人工审批集成 | LLM+OSS API、MCP 运维工具链、HITL 审批流 | [KubeCon HolmesGPT 案例](http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49) |

##### 第三类：超越连接新服务

| 场景 | 关键指标诉求 | 主要挑战 | 技术诉求 | 参考链接 |
|------|-----------|---------|---------|---------|
| **个人数字智能助理**（类 OpenClaw 本地 Agent） | 个人数据完全保护、离线可用、跨 APP 智能联动 | 隐私保护与能力之间的平衡、边缘推理性能 | 端侧小模型推理、隐私计算、个人 MCP 服务器 | [Anthropic Claude](https://www.anthropic.com/claude) |
| **手机智能体**（豆包/小艺类） | 系统级 Agent 集成、全 APP 覆盖、响应 <500ms | 系统权限开放与安全、跨 APP 数据隔离 | OS 级 Agent API、端侧推理加速框架 | [豆包 Agent](https://team.doubao.com/en/special/agent) |
| **编码智能体**（Claude Code 类） | SWE-bench >50%、自主完成复杂 PR、长任务可靠性 | 长任务上下文管理、代码安全性保障 | Harness Engineering、全项目 RAG、沙箱执行 | [The Rise of Coding Agents](https://www.anthropic.com/research/coding-agents) |
| **办公智能体**（Microsoft Copilot 类） | 企业数据合规、多格式文档无缝处理、准确率 >90% | 企业数据隐私保护、复杂工具链集成 | 企业 RAG、安全知识图谱、M365 深度集成 | [M365 Copilot](https://adoption.microsoft.com/en-us/microsoft-365-copilot/) |

---

### 2.3 AI 原生平台

#### AI Native 平台分层架构图

```
北向 ──────────────────────────────────────────────────────────────
   6G Agent NF 应用层：连接ANF | 数据ANF | 系统Agent | 超越连接ANF | 行业ANF
   服务化应用层：传统微服务应用 | REST API 应用
────────────────────────────────────────────────────────────────────
                          ↕ 标准化接口（MCP/A2A/REST）
====================================================================
              AI Native 平台（中间层）
====================================================================

  +---------------------------+   +--------------------------+
  |        AI 平台              |   |        云平台              |
  |                           |   |                          |
  | +----------------------+  |   | +--------------------+  |
  | |      Agent 平台        |  |   | |   领域云原生平台     |  |
  | |                      |  |   | |                    |  |
  | | • Agent 开发编排框架  |  |   | | • 微服务开发框架    |  |
  | |   LangGraph/ADK/     |  |   | |   Spring Boot/Go   |  |
  | |   AutoGen            |  |   | | • 分布式运行框架    |  |
  | | • Harness 运行框架   |  |   | |   Service Mesh/    |  |
  | |   OpenClaw/Deep      |  |   | |   Istio/Envoy      |  |
  | |   Agents/Deer-Flow   |  |   | | • 微服务治理        |  |
  | | • Agent 治理框架     |  |   | |   注册发现/可靠性   |  |
  | |   Agentic Mesh/      |  |   | +--------------------+  |
  | |   Coze/小艺智能体平台 |  |   |                          |
  | | • 元能力服务          |  |   | +--------------------+  |
  | |   向量DB/记忆服务/   |  |   | |    电信云平台         |  |
  | |   MCP 工具服务        |  |   | |                    |  |
  | +----------------------+  |   | | • K8s 容器治理      |  |
  |                           |   | | • OpenStack VM 治理 |  |
  | +----------------------+  |   | | • 计算/存储/网络    |  |
  | |    模型推理平台          |  |   | |   虚拟化           |  |
  | |                      |  |   | +--------------------+  |
  | | • 推理框架             |  |   |                          |
  | |   vLLM / SGLang      |  |   +--------------------------+
  | | • 算子算法加速         |  |
  | |   TensorRT-LLM/Flash |  |
  | |   Attention          |  |
  | | • 分布式推理           |  |
  | |   Dynamo / llm-d     |  |
  | +----------------------+  |
  +---------------------------+

====================================================================
南向 ─────────── COTS 硬件 ─────────────────────────────────────────
   x86 服务器 | ARM 服务器 | NVIDIA GPU | 昇腾 NPU | DPU | 智能网卡
────────────────────────────────────────────────────────────────────
```

#### Agent 平台关键组件与参考实现

| 组件 | 核心功能 | 参考实现 | 链接 |
|------|---------|---------|------|
| Agent 开发编排框架 | 定义 Agent 工作流图，支持有状态执行、HITL、子 Agent | LangGraph | [https://github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) |
| Harness 运行框架 | 提供 Context/Model/Skills/Eval/Sandbox Agent Loop | DeepAgents / Deer-Flow | [https://github.com/langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) |
| Agent 治理框架 | Agent 注册发现、可靠性、访问控制、多租户 | Coze / 华为小艺智能体平台 | [https://coze.com/](https://coze.com/) |
| 向量数据库 | 语义检索、RAG 知识存储 | Chroma / Weaviate / Milvus | [https://github.com/chroma-core/chroma](https://github.com/chroma-core/chroma) |
| MCP 工具服务 | 标准化工具接口，连接外部系统和数据 | MCP / LiteLLM | [https://github.com/modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol) |

#### 模型推理平台关键组件与参考实现

| 组件 | 核心功能 | 参考实现 | 链接 |
|------|---------|---------|------|
| 推理框架 | 高性能 LLM 推理，连续批处理，支持 PagedAttention | vLLM / SGLang | [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm) |
| 算子算法加速 | 算子融合、量化（INT4/INT8）、Flash Attention 优化 | TensorRT-LLM | [https://github.com/NVIDIA/TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) |
| 分布式推理框架 | 跨节点/跨集群 LLM 推理调度、prefill-decode 分离 | Dynamo / llm-d | [https://github.com/ai-dynamo/dynamo](https://github.com/ai-dynamo/dynamo) |

参考：llm-d 跨集群联邦推理（KubeCon EU 2026）：[http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd)

#### 平台 Agent（支撑应用 Agent 全生命周期）

AI 原生平台提供支撑应用 Agent 全生命周期的平台 Agent，通过 agent.md / soul.md 动态更新规范和原则：

| 平台 Agent | 主要功能 | agent.md 配置 | soul.md 配置 |
|-----------|---------|--------------|-------------|
| **设计 Agent** | AI 辅助需求分析、架构设计、功能设计、接口设计 | 能力范围、需求分析模板、设计输出格式 | 架构规范、设计原则、合规约束 |
| **开发 Agent** | AI 辅助编码、代码审查、重构、技术债管理 | 编码范围、代码生成规则、工具列表 | 编程规范、代码质量标准、安全约束 |
| **测试 Agent** | AI 辅助测试用例设计、执行、缺陷分析、质量评估 | 测试范围、用例设计模板、执行策略 | 测试标准、覆盖率要求、质量门禁 |
| **部署 Agent** | AI 辅助部署策略制定、脚本生成、执行和验证 | 部署范围、脚本模板、验证策略 | 部署规范、变更约束、回滚原则 |
| **运行 Agent** | 运行时监控、性能优化、故障检测与自动恢复 | 监控范围、告警规则、处置策略 | SLA 规范、自愈边界、安全约束 |
| **运维 Agent** | 意图驱动运维操作、配置管理、容量规划 | 运维操作范围、意图解析规则 | 运维规范、操作约束、审计要求 |

#### Agent Harness 运行时（Agent Loop 自进化智能环）

```
+===============================================================+
|              Agent Harness 运行时                               |
|                                                                 |
|  +-----------------------------------------------------------+ |
|  |          Agent Loop 自进化智能环                             | |
|  |                                                           | |
|  |  +--------+  +--------+  +--------+  +--------+         | |
|  |  | 上下文  |->|  模型   |->| Skills |->|  评估  |         | |
|  |  | Context|  | Router |  | Engine |  |  Eval  |         | |
|  |  +--------+  +--------+  +--------+  +---+----+         | |
|  |      ^                                   |               | |
|  |      |         +----------+              |               | |
|  |      |         | 运行沙箱  |<-------------+               | |
|  |      |         | Sandbox  |                              | |
|  |      |         +----+-----+                              | |
|  |      |              |                                    | |
|  |      +----- 自进化反馈环 --------------------------------+ | |
|  |                                                           | |
|  | 自进化能力：                                                | |
|  | • 上下文：Prompt 动态优化 + RAG 自适应检索                   | |
|  | • 模型：基于任务质量自动切换最优模型                           | |
|  | • Skills：从任务执行中自动学习并创建新 Skill                  | |
|  +-----------------------------------------------------------+ |
|                                                                 |
|  关键竞争力：精度(Accuracy) + 确定性(Determinism) + E2E 时延    |
+===============================================================+
```

参考：
- Darwin Gödel Machine（Harness 自进化，SWE-bench 从 20% 提升到 50%）：[https://arxiv.org/abs/2505.22954](https://arxiv.org/abs/2505.22954)
- Kubernetes Agent Sandbox：[https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/)

#### Cloud Native 平台 vs AI Native 平台技术栈对比

| 层次 | Cloud Native 平台（CNCF 定义） | AI Native 平台 | 关键变化 |
|------|------------------------------|---------------|---------|
| **应用层** | 微服务应用（容器化） | Agent NF + 微服务应用 | 新增 Agent 服务类型，Agent 具备自主决策能力 |
| **编排层** | Kubernetes（资源调度） | Kubernetes + Agent 编排（LangGraph） | 双层编排：资源层（K8s）+ 意图层（Agent） |
| **运行框架** | Service Mesh（Istio/Envoy） | Service Mesh + Harness 运行时 | 新增 AI Harness 层，支持 Agent Loop |
| **通信协议** | HTTP/gRPC/消息队列 | HTTP/gRPC + MCP/A2A + 语义路由 | 新增 AI 语义通信协议层 |
| **存储** | 关系型 DB + 对象存储 + 缓存 | 关系型 DB + 向量 DB + 对象存储 + 记忆存储 | 新增向量数据库和 Agent 记忆持久化 |
| **计算** | CPU 通用计算（x86/ARM） | CPU + GPU + NPU + 专用 AI 芯片 | 异构计算支持，GPU/NPU 成为一等公民 |
| **可观测性** | OTel（日志/指标/追踪） | OTel + LLM 追踪 + Eval 指标 + Agent 审计 | 新增 AI 特有可观测性：Token 消耗、推理质量 |
| **安全** | RBAC + mTLS + 网络策略 | RBAC + MCP 授权 + OIDC + Sandbox + AI 审计 | 新增 AI 操作安全：工具权限控制、沙箱隔离 |
| **CI/CD** | GitOps + 流水线（Tekton/Argo） | GitOps + AI Harness 测试 + Eval CI | 新增 AI 评估门禁，Evals 作为发布条件 |

