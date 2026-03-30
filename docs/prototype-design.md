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


---

## 三、开发

### 洞察

#### 3.1.1 开发模式对比洞察

| 对比维度 | 传统微服务开发模式 | AI 辅助开发模式 | Harness Engineering 开发模式 |
|---------|-----------------|----------------|---------------------------|
| **设计阶段** | 人工需求分析、架构评审、UML 建模 | AI 生成架构建议、自动生成 UML、AI Review | 设计 Agent 自主分析需求、自动生成设计文档、Skills 调用专业检查工具 |
| **编码阶段** | 全手工编码、代码审查依赖 IDE 插件 | Copilot/Cursor 辅助补全、局部生成 | 编码 Agent 自主完成整个功能、基于 agent.md 遵循编码规范 |
| **开发态测试** | 手工编写单元测试、人工执行 | AI 生成测试用例、人工确认 | 测试 Agent 自主设计测试策略、执行测试并分析结果、Eval Loop 自动评估质量 |
| **开发态部署** | 手工编写 Dockerfile/Helm、Jenkins 流水线 | AI 生成部署脚本、人工审核 | 部署 Agent 自主生成部署方案、执行部署并拨测验证 |
| **面临挑战** | 效率低、质量依赖个人能力、知识孤岛 | AI 建议不稳定、需大量人工确认、集成复杂 | Harness 设计复杂、Agent 可靠性保障、Eval 体系建立成本高 |

**平台开发框架实现**：
- 传统模式：Spring Boot + Maven + Jenkins + SonarQube（[https://spring.io/projects/spring-boot](https://spring.io/projects/spring-boot)）
- AI 辅助模式：GitHub Copilot + Cursor + Claude Code（[https://github.blog/ai-and-ml/github-copilot/](https://github.blog/ai-and-ml/github-copilot/)）
- Harness Engineering 模式：LangGraph + DeepAgents + OpenClaw + agent.md/soul.md（[https://github.com/langchain-ai/deepagents](https://github.com/langchain-ai/deepagents)）

**关键竞争力构筑点**：

| 模式 | 竞争力构筑点 | 效果数据 |
|------|-----------|---------|
| 传统微服务 | 标准化框架、成熟工具链、可靠性 | 开发效率基线 |
| AI 辅助开发 | AI 代码补全、文档生成、初步自动化 | 开发效率提升 20-40%（GitHub Copilot 数据：[https://github.blog/news-insights/research/quantifying-github-copilots-impact-on-developer-productivity-and-happiness/](https://github.blog/news-insights/research/quantifying-github-copilots-impact-on-developer-productivity-and-happiness/)） |
| Harness Engineering | Agent 自主完成任务、Eval 持续优化、Skills 知识复用 | 开发效率提升 3-5x（理论上限，基于 SWE-bench 50%+ 自主解决率）|

---

#### 3.1.2 业务诉求洞察

结合 6G Core + AI Native 架构 + 6G UC 场景，对开发框架的核心诉求：

| 诉求维度 | 6G Core 特殊诉求 | 业界实践参考 |
|---------|----------------|------------|
| **异构计算支持** | 需同时支持 CPU 微服务、GPU/NPU Agent 推理、DSP 信号处理 | Ray 异构分布式框架：[https://docs.ray.io/en/latest/](https://docs.ray.io/en/latest/) |
| **实时性能** | 核心网控制面 <10ms、用户面 <1ms、意图引擎 <100ms | SGLang 推理加速：[https://github.com/sgl-project/sglang](https://github.com/sgl-project/sglang) |
| **高可靠性** | 5 个 9（99.999%）以上可靠性，故障自愈 | OpenStack Masakari 自愈：[https://wiki.openstack.org/wiki/Masakari](https://wiki.openstack.org/wiki/Masakari) |
| **安全合规** | 电信级安全（3GPP SECAM）、数据主权保护 | Zero Trust 架构：[https://www.nist.gov/publications/zero-trust-architecture](https://www.nist.gov/publications/zero-trust-architecture) |
| **AI 代码与传统代码共存** | AI 生成的 Agent 逻辑与传统信令处理代码需要安全共存 | 人工代码给 AI 代码兜底：[https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) |

**开发框架关键技术挑战和命题**：
1. **异构编程统一抽象**：如何在一个开发框架中统一表达 CPU 微服务、GPU 推理、信号处理？
2. **确定性与 AI 随机性**：如何在 AI 生成代码中保障电信级确定性？
3. **AI-人工代码边界**：AI 生成代码和人工编写代码如何安全共存、相互兜底？

---

#### 3.1.3 技术趋势洞察

**异构分布式编程框架实践**：

| 框架 | 核心特点 | 适用场景 | 参考链接 |
|------|---------|---------|---------|
| **Ray** | Actor 模型 + 任务图，原生支持 GPU/CPU 异构 | 大规模分布式 AI 推理、强化学习训练 | [https://github.com/ray-project/ray](https://github.com/ray-project/ray) |
| **OpenYuanRong（开元融）** | 华为开源的异构计算框架，支持昇腾 NPU | 电信网络 AI 推理、边缘计算 | [https://gitee.com/open_euler/discussion/issues/I5V6XZ](https://gitee.com/open_euler/discussion/issues/I5V6XZ) |
| **Service Weaver** | Google 开源，以内存语义替代网络通信，部署时自动决定拆分粒度 | 微服务 → Monolith 自动切换，减少网络开销 | [https://github.com/ServiceWeaver/weaver](https://github.com/ServiceWeaver/weaver) |

**以内存为中心的编程实践**：
- Service Weaver 提出 "代码当单体写，运行时可拆分" 理念（[https://serviceweaver.dev/blog/towards_modern_development_of_cloud_applications.html](https://serviceweaver.dev/blog/towards_modern_development_of_cloud_applications.html)）
- Unikraft 单内核操作系统（极低内存占用，适合边缘 Agent）：[https://github.com/unikraft/unikraft](https://github.com/unikraft/unikraft)

**AI 生成代码与运维/可靠性代码融合实践**：

| 实践方向 | 挑战 | 业界方案 | 参考链接 |
|---------|------|---------|---------|
| AI 生成业务逻辑 + 人工编写可靠性框架 | AI 代码不遵循可靠性约束 | 通过 soul.md 注入可靠性规范，约束 AI 行为 | [https://www.anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents) |
| AI 生成测试 + 人工验证关键路径 | AI 测试覆盖率不均匀 | SWE-bench 驱动 Agent 测试能力持续提升 | [https://arxiv.org/abs/2310.06770](https://arxiv.org/abs/2310.06770) |
| AI 生成代码的运行时安全验证 | AI 代码可能产生意外行为 | Sandbox 隔离执行 + 行为审计 | [https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/) |

---

#### 3.1.4 开发框架构想

结合 AI 编程、OpenClaw 实践、Harness Engineering 洞察，平台开发框架构筑方向：

```
开发框架分层：
+----------------------------------------------------------+
|  应用层 Agent             平台层 Agent                     |
|  - 应用设计 Agent          - 平台设计 Agent               |
|  - 应用编码 Agent          - 平台编码 Agent               |
|  - 应用测试 Agent          - 平台测试 Agent               |
|  - 应用部署 Agent          - 平台部署 Agent               |
+----------------------------------------------------------+
|              开发框架核心能力                               |
|  AI 辅助研发 + 异构编程 + 确定性保障 + 可靠性框架 + 安全   |
+----------------------------------------------------------+
```

**AI 辅助研发之外，还需要构筑的能力**：
1. **异构计算抽象**：统一 CPU/GPU/NPU 编程接口（参考 Ray：[https://docs.ray.io/en/latest/](https://docs.ray.io/en/latest/)）
2. **确定性框架**：在 AI 随机性之上构建确定性执行层（TSN/RTOS 集成）
3. **可靠性内建**：断路器、熔断、重试、降级内置于框架（参考 Resilience4j：[https://github.com/resilience4j/resilience4j](https://github.com/resilience4j/resilience4j)）
4. **安全沙箱**：AI 生成代码的安全执行环境（参考 Firecracker MicroVM：[https://github.com/firecracker-microvm/firecracker](https://github.com/firecracker-microvm/firecracker)）

---

### 3.2 设计 Agent

#### 洞察

**主要功能**：
- 需求分析：从用户故事/需求文档自动生成结构化需求规格
- 架构设计：基于 AI Native/6G 架构规范自动生成架构方案
- 接口设计：自动生成 API 规范（OpenAPI/Protobuf）
- 风险识别：自动检查架构合规性、安全性、可靠性风险

**关键问题**：
- 需求歧义消除：多轮对话澄清需求意图
- 架构约束注入：通过 soul.md 注入架构原则，避免违规设计
- 设计一致性：多个 Agent 协作设计时保持全局一致性

**技术挑战**：
- 大型系统的架构知识图谱构建和查询
- 领域特定架构规范的形式化表达

**业界优秀实践**：
- GitHub Copilot Workspace（设计到代码全流程）：[https://githubnext.com/projects/copilot-workspace](https://githubnext.com/projects/copilot-workspace)
- Devin（自主软件工程师，包含设计能力）：[https://www.cognition.ai/blog/introducing-devin](https://www.cognition.ai/blog/introducing-devin)
- AI Scientist v2（端到端自主研究设计）：[https://github.com/SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)

#### 设计 Agent Playground

**agent.md（设计 Agent）**：
```markdown
# 设计 Agent 能力范围
你是 6G Core 应用的设计 Agent，负责分析需求并生成符合 AI Native 架构规范的设计方案。

## 能力范围
- 需求分析：解析用户需求，识别功能需求和非功能需求
- 架构设计：生成符合 AI Native 架构的 Agent NF 设计方案
- 接口设计：生成 MCP/REST/gRPC 接口规范
- 风险评估：识别架构风险和安全漏洞

## 需求分析 Prompt
分析以下需求，提取：功能需求列表、非功能需求（性能/可靠性/安全/可维护性）、外部依赖、约束条件

## 架构设计 Prompt
基于需求分析结果，参考 soul.md 中的架构规范，生成：Agent NF 设计、数据流图、接口清单

## 功能设计 Prompt
为每个 Agent NF 详细设计：内部模块划分、Skills 列表、状态机、错误处理策略

## 软件实现设计 Prompt
生成实现指导：技术选型、关键算法、数据结构、并发模型、依赖关系
```

**soul.md（设计 Agent）**：
```markdown
# 架构规范与原则（Design Agent Soul）
## 核心架构原则
- AI Native First：所有新组件优先设计为 Agent，通过 Skills 扩展能力
- 模型解耦：Agent 不依赖特定模型，通过 Model Router 支持模型切换
- Harness 优先：业务逻辑通过 Harness 层封装，确保可靠性和可测试性

## 6G 核心网约束
- 控制面时延：< 10ms
- 用户面时延：< 1ms
- 可靠性：> 99.999%（5 个 9）
- 安全：遵循 3GPP SECAM 安全规范

## 设计禁止项
- 禁止设计与特定模型强耦合的接口
- 禁止设计无沙箱隔离的代码执行路径
- 禁止跳过 Eval 门禁直接部署到生产
```

**Skills 清单（设计 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `architecture_check_skill` | 检查设计方案是否符合 AI Native 架构规范 | `architecture_check(design_doc)` |
| `scenario_query_skill` | 查询 6G UC 场景库，匹配相关场景需求 | `query_scenario(intent="XR 沉浸式")` |
| `performance_spec_skill` | 查询性能规格库（时延/带宽/可靠性指标） | `get_perf_spec(nf_type="AMF")` |
| `serviceability_skill` | 查询可服务性要求（升级/扩容/备份策略） | `check_serviceability(design)` |
| `fault_pattern_skill` | 查询故障模式库，识别设计中的故障风险 | `analyze_fault_pattern(design)` |
| `security_analysis_skill` | 安全分析（威胁建模、漏洞识别） | `security_analysis(design_doc)` |
| `interface_query_skill` | 查询外部交互接口规范（3GPP/ETSI 标准） | `query_interface(protocol="N1")` |

---

### 3.3 编码 Agent

#### 洞察

**主要功能**：
- 基于设计文档自动生成完整功能代码
- 代码审查：检查代码质量、安全性、性能
- 重构建议：识别技术债，提出重构方案
- 代码解释：为复杂代码生成注释和文档

**关键问题**：
- 生成代码与已有代码风格一致性（通过 soul.md 注入编码规范）
- AI 生成代码的安全性（SQL 注入、缓冲区溢出等）
- 长文件和复杂依赖的处理

**技术挑战**：
- 全项目代码库的语义理解（超过 100K 行代码时的性能）
- AI 代码与人工代码的合并冲突处理

**业界优秀实践**：
- Claude Code 自主完成整个 PR（SWE-bench 50%+）：[https://www.anthropic.com/research/coding-agents](https://www.anthropic.com/research/coding-agents)
- open-swe（基于 LangGraph 的异步软件工程 Agent）：[https://github.com/langchain-ai/open-swe](https://github.com/langchain-ai/open-swe)
- DeepAgents（内置规划/文件/Shell 的编码 Agent）：[https://github.com/langchain-ai/deepagents](https://github.com/langchain-ai/deepagents)
- Darwin Gödel Machine（自进化编程 Agent，80 轮迭代 SWE-bench 从 20% 到 50%）：[https://arxiv.org/abs/2505.22954](https://arxiv.org/abs/2505.22954)

#### 编码 Agent Playground

**agent.md（编码 Agent）**：
```markdown
# 编码 Agent 能力范围
你是 6G Core 应用的编码 Agent，负责根据设计文档生成高质量代码。

## 能力范围
- 功能实现：根据设计文档生成完整的业务逻辑代码
- 代码审查：检查代码质量、安全性、合规性
- 单元测试：为生成的代码自动生成单元测试
- 文档生成：为代码生成 API 文档和注释

## 编码 Prompt
根据以下设计规格，生成代码：
1. 严格遵循 soul.md 中的编码规范
2. 优先使用框架提供的已有 Skills 和 API，避免重复实现
3. 所有公共接口必须有错误处理和日志
4. 性能敏感路径避免不必要的对象分配
```

**soul.md（编码 Agent）**：
```markdown
# 编码规范（Coding Agent Soul）
## 通用规范
- 语言：Go（控制面）/ C++（用户面）/ Python（AI 逻辑）
- 代码风格：遵循 Google Style Guide
- 错误处理：所有错误必须显式处理，禁止静默忽略
- 日志：结构化日志（JSON），包含 TraceID

## 安全编码规范
- 禁止 SQL 拼接，必须使用参数化查询
- 所有外部输入必须校验和净化
- 敏感数据禁止明文日志

## 性能规范
- 热路径：禁止内存分配，使用对象池
- 并发：使用无锁数据结构，避免全局锁
- 超时：所有外部调用必须设置超时（最大 5s）
```

**Skills 清单（编码 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `clean_code_check_skill` | 检查代码质量（圈复杂度、命名规范、重复代码） | `clean_code_check(code_file)` |
| `security_scan_skill` | 代码安全扫描（SAST，检测常见漏洞） | `security_scan(repo_path)` |
| `amf_sm_api_skill` | 调用核心网 AMF/SMF 已有 API | `amf_register_ue(ue_id, plmn)` |
| `mcp_tool_call_skill` | 通过 MCP 协议调用外部工具 | `mcp_call(tool="database", action="query")` |
| `code_review_skill` | AI 代码审查，给出改进建议 | `review_code(pr_diff)` |
| `test_gen_skill` | 自动为代码生成单元测试 | `generate_tests(function_code)` |

---

### 3.4 开发态测试 Agent

#### 洞察

**主要功能**：
- 测试策略制定：基于代码变更范围自动确定测试策略
- 测试用例生成：自动生成单元测试、集成测试、边界测试
- 测试执行与分析：执行测试并分析失败原因
- 测试质量评估：评估测试覆盖率和测试有效性

**关键问题**：
- AI 生成测试的质量评估（避免无效测试）
- 测试与被测代码的同步更新
- 非确定性 AI 输出的测试策略

**技术挑战**：
- AI 测试 Agent 的 Eval 闭环设计（用 Eval 评估 Eval）
- 电信级功能验证（协议栈、状态机测试）

**业界优秀实践**：
- OpenAI Evals 框架（LLM 评估标准化）：[https://github.com/openai/evals](https://github.com/openai/evals)
- Agent-as-a-Judge（Agent 评估 Agent）：[https://arxiv.org/abs/2410.10934](https://arxiv.org/abs/2410.10934)
- SWE-bench（真实 GitHub Issue 测试基准）：[https://arxiv.org/abs/2310.06770](https://arxiv.org/abs/2310.06770)
- LLM Evals（Martin Fowler 系统介绍）：[https://martinfowler.com/articles/llm-evals.html](https://martinfowler.com/articles/llm-evals.html)

#### 开发态测试 Agent Playground

**agent.md（开发态测试 Agent）**：
```markdown
# 测试 Agent 能力范围
你是 6G Core 应用的开发态测试 Agent，负责保障代码质量。

## 能力范围
- 测试策略：分析代码变更，制定最优测试策略（最小化测试集，最大化覆盖率）
- 用例设计：生成功能测试、边界测试、异常测试、性能测试用例
- 用例编码：将测试用例转化为可执行的测试代码（Go test / pytest）
- 结果分析：分析测试失败原因，给出修复建议

## 测试用例设计 Prompt
基于代码变更，识别测试范围：
1. 新增/修改的接口（必须覆盖）
2. 影响到的下游调用（需要回归测试）
3. 边界条件（空值、最大值、并发）
4. 错误路径（所有错误分支都必须测试）
```

**soul.md（开发态测试 Agent）**：
```markdown
# 测试规范（Test Agent Soul）
## 测试覆盖要求
- 单元测试覆盖率：>85%（核心逻辑 >95%）
- 错误路径覆盖率：100%
- 并发测试：所有共享状态必须包含并发测试

## 测试质量标准
- 每个测试只验证一个行为（单一职责）
- 测试命名：Test_功能名称_场景_期望结果
- 禁止在测试中使用 time.Sleep（使用 mock）

## 电信协议测试规范
- 信令流程测试：必须覆盖 3GPP 规定的所有正常/异常流程
- 状态机测试：覆盖所有状态转换路径
```

**Skills 清单（开发态测试 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `scenario_query_skill` | 查询测试场景库（6G 协议场景、UC 场景） | `query_test_scenario(nf="AMF", flow="registration")` |
| `test_case_lib_skill` | 查询历史测试用例库 | `find_similar_tests(feature_desc)` |
| `test_report_skill` | 生成测试报告（覆盖率、通过率、风险点） | `generate_test_report(results)` |
| `failure_analysis_skill` | 分析测试失败原因，给出修复建议 | `analyze_failure(test_log)` |
| `coverage_check_skill` | 检查测试覆盖率，识别覆盖盲区 | `check_coverage(coverage_report)` |
| `perf_test_skill` | 性能测试（TPS、时延、资源占用） | `run_perf_test(scenario, target_tps=1000)` |

---

### 3.5 开发态部署 Agent

#### 洞察

**主要功能**：
- 部署方案生成：基于代码和配置自动生成 Kubernetes/Helm 部署方案
- 部署脚本生成：自动生成 CI/CD 脚本
- 部署执行：自动执行开发环境部署
- 部署验证（拨测）：部署后自动验证功能正确性

**关键问题**：
- 开发环境与生产环境的差异管理
- AI 生成部署脚本的安全审查
- 快速迭代场景下的增量部署

**技术挑战**：
- 多集群、多环境部署的一致性
- AI Agent 部署操作的权限边界控制

**业界优秀实践**：
- GitOps + Flux MCP + AI Agents（KubeCon EU 2026）：[http://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759](http://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759)
- Agentic GitOps（ControlPlane，KubeCon EU 2026）：[http://kccnceu2026.sched.com/event/55bd23423789cd1d328edf6bb67f770d](http://kccnceu2026.sched.com/event/55bd23423789cd1d328edf6bb67f770d)
- Building IDP in 5 Minutes（Port，KubeCon EU 2026）：[http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49](http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49)

#### 开发态部署 Agent Playground

**agent.md（开发态部署 Agent）**：
```markdown
# 部署 Agent 能力范围（开发态）
负责 6G Core 应用在开发环境的自动化部署。

## 能力范围
- 部署方案生成：分析应用配置，生成 Helm Chart/Kubernetes YAML
- CI/CD 脚本生成：生成 GitHub Actions/Tekton 流水线
- 开发环境部署：执行到开发 K8s 集群的自动部署
- 部署验证：部署后执行拨测，确认服务正常

## 部署脚本生成 Prompt
根据以下应用信息，生成 Kubernetes 部署配置：
- 遵循 soul.md 中的部署规范
- 为 Agent 组件配置 GPU 资源请求
- 设置合理的 readiness/liveness 探针
- 配置适当的资源 limits/requests

## 部署验证 Prompt
部署完成后，执行以下验证：
1. Pod 全部 Running 且 Ready
2. 基础连通性验证（health check）
3. 关键 API 功能验证（smoke test）
4. 性能基线检查（P99 时延 < 阈值）
```

**soul.md（开发态部署 Agent）**：
```markdown
# 部署规范（Deploy Agent Soul - 开发态）
## 开发环境部署原则
- 资源限制：开发环境 CPU/内存 Limit 为生产的 20%
- 副本数：开发环境单副本（生产 3 副本以上）
- 镜像：使用 :dev 标签，禁止使用 latest

## 安全约束
- 禁止部署到生产命名空间（prod-*)
- 所有 Agent 组件必须配置 securityContext（非 root 运行）
- 禁止 hostNetwork 和 privileged 模式

## 变更管理
- 所有部署变更必须通过 GitOps（Flux/ArgoCD）执行
- 部署前必须通过 CI 测试门禁
- 生产部署必须有人工审批（HITL）
```

**Skills 清单（开发态部署 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `deploy_scenario_skill` | 查询部署场景库，获取最佳部署模式 | `query_deploy_scenario(app_type="agent-nf")` |
| `helm_template_skill` | 查询和生成 Helm Chart 模板 | `generate_helm_chart(app_config)` |
| `kubectl_exec_skill` | 执行 kubectl 命令进行部署 | `kubectl_apply(manifest_path, namespace="dev")` |
| `health_check_skill` | 部署后健康检查（Pod/Service/Endpoint 状态） | `check_health(deployment_name)` |
| `smoke_test_skill` | 执行 smoke test 验证关键功能 | `run_smoke_test(service_url, test_cases)` |
| `rollback_skill` | 部署失败时自动回滚 | `rollback(deployment_name, revision)` |


---

## 四、测试

### 洞察

#### 4.1.1 评测模式对比洞察

| 对比维度 | 传统软件测试（自动化评测） | Agent 智能体验评测（AI 辅助评测） | 关键差异说明 |
|---------|----------------------|-------------------------------|-----------|
| **测试标准** | IEEE 829 测试文档标准、ISTQB 测试方法 | LLM Evals 框架（规则/LLM-Judge/人工） | 新增 AI 特有评估维度（幻觉率、一致性） |
| **评测方案** | 测试用例 + 预期结果（确定性） | 测试场景 + 评分标准（非确定性） | 从 Pass/Fail 到多维度打分 |
| **评测技术** | 单元/集成/E2E 自动化测试（Selenium/JUnit） | Agent-as-Judge、LLM-as-Evaluator、基准测试 | 新增智能评测引擎 |
| **测试数据** | 固定测试数据集 | 动态生成测试场景 + 人工标注黄金集 | 测试数据生成能力成为关键 |
| **评测效率** | 自动化后效率高，但维护成本高 | AI 可自动生成测试用例，减少维护成本 | AI 生成测试 + 人工验证关键路径 |

**下一代评测诉求和关键命题**：
1. 如何评测 Agent 的"意图理解准确率"？（非传统 API 测试）
2. 非确定性输出如何建立稳定的质量基线？
3. 如何实现 Agent 评测的持续自动化（CI/CD 集成）？

参考：
- LLM Evals 系统介绍（Martin Fowler）：[https://martinfowler.com/articles/llm-evals.html](https://martinfowler.com/articles/llm-evals.html)
- Agent-as-a-Judge 框架：[https://arxiv.org/abs/2410.10934](https://arxiv.org/abs/2410.10934)
- LLM 评估综合综述：[https://arxiv.org/abs/2310.19736](https://arxiv.org/abs/2310.19736)

---

#### 4.1.2 业务诉求洞察

**5GC vs 6G 业务场景测试差异**：

| 测试维度 | 5GC 测试 | 6G 测试 | 关键变化 |
|---------|---------|---------|---------|
| **测试对象** | 确定性网元（AMF/SMF/UPF） | Agent NF（概率性决策） | 需要 Agent 评测框架而非传统功能测试 |
| **协议测试** | 3GPP TS 38 系列协议一致性 | 3GPP 6G + 意图协议 + ACN 协议 | 需要意图理解准确性测试 |
| **性能基线** | 3GPP 定义的 KPI（时延/吞吐/可靠性） | 6G KPI + Agent 精度 + 意图满足率 | 新增 AI 特有 KPI |
| **安全测试** | 电信安全（3GPP SECAM） | 电信安全 + AI 安全（对抗攻击/提示注入） | 新增 AI 特有安全测试 |
| **互操作测试** | 标准协议互操作（IOT） | IOT + Agent 协议互操作 + MCP 互操作 | 新增 MCP/A2A 协议互操作测试 |

**6G 场景下评测诉求**：
- 意图识别准确率 > 95%（评测难点：意图表达多样性）
- 端到端业务开通时延 < 3s（评测要求：包含 AI 推理时间）
- 自愈成功率 > 90%（评测要求：覆盖各类故障场景）

参考：
- 3GPP 6G 用例场景：[https://www.3gpp.org/ftp/Specs/archive/22_series/22.847/](https://www.3gpp.org/ftp/Specs/archive/22_series/22.847/)
- TMForum 意图驱动网络测试：[https://www.tmforum.org/intent-nbi/](https://www.tmforum.org/intent-nbi/)

---

#### 4.1.3 技术趋势洞察

**Cloud Native vs AI Native 测试技术对比**：

| 测试维度 | Cloud Native 测试 | AI Native 测试 | 关键差异 |
|---------|-----------------|---------------|---------|
| **单元测试** | JUnit/Go test/pytest（确定性） | 基于 Eval 的 Agent 单元测试（非确定性） | 新增 AI 输出的多维度评分 |
| **集成测试** | 服务间 API 测试（契约测试） | Agent 协作测试（任务分解+协调验证） | 测试 Agent 间的意图传递准确性 |
| **E2E 测试** | Selenium/Cypress（UI）/ k6（性能） | 意图驱动 E2E 测试（自然语言描述测试意图） | 测试脚本从代码变为自然语言 |
| **混沌工程** | Chaos Monkey/Litmus（基础设施故障） | AI 混沌（模型 API 故障/幻觉注入） | 新增 AI 特有故障类型 |
| **测试数据** | 固定 Fixture / 数据库快照 | AI 合成测试数据（覆盖边界场景） | AI 自动生成测试数据 |

**优秀实践**：
- OpenAI Evals（LLM 评估框架）：[https://github.com/openai/evals](https://github.com/openai/evals)
- Anthropic Cookbook（Claude 评估示例）：[https://github.com/anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook)
- Patterns for LLM Systems（Eugene Yan，Evals 最佳实践）：[https://eugeneyan.com/writing/llm-patterns](https://eugeneyan.com/writing/llm-patterns)

---

### 4.2 评测 Agent

#### 洞察

**主要功能**：评测标准管理、评测方案设计、评测指标数据查询、评测结果分析

**关键问题**：
- 如何设计对 AI Agent 行为的客观评测标准
- 如何处理 Agent 输出的非确定性（同一输入可能有多个正确输出）
- 评测基准的持续更新（防止 Goodhart 定律：当指标成为目标，它就不再是好指标）

**业界优秀实践**：
- SWE-bench（真实 GitHub 评测基准）：[https://arxiv.org/abs/2310.06770](https://arxiv.org/abs/2310.06770)（Claude Code 在此基准达 50%+）
- MMLU（多任务语言理解基准）：[https://arxiv.org/abs/2009.03300](https://arxiv.org/abs/2009.03300)
- HellaSwag/HumanEval（代码评测）：[https://github.com/openai/human-eval](https://github.com/openai/human-eval)

#### 评测 Agent Playground

**agent.md（评测 Agent）**：
```markdown
# 评测 Agent 能力范围
负责制定和执行 6G Core Agent NF 的评测方案。

## 能力范围
- 评测标准制定：基于 3GPP/TMForum 标准和 AI 评测框架制定评测指标
- 评测方案设计：针对不同 Agent NF 设计专项评测方案
- 评测执行：协调测试执行并收集评测数据
- 结果分析：多维度分析评测结果，识别质量风险
```

**soul.md（评测 Agent）**：
```markdown
# 评测规范（Evaluation Agent Soul）
## 核心评测维度
- 功能正确性：Agent 输出是否满足业务需求（准确率 > 95%）
- 一致性：相同输入的输出是否稳定（方差 < 5%）
- 安全性：Agent 是否遵循安全约束（0 违规）
- 性能：响应时间是否满足 SLA（P99 < 阈值）

## 评测标准来源
- 3GPP TS 33.501（5G 安全架构）
- 3GPP TR 22.847（6G 用例和需求）
- TMForum IG1194（意图驱动网络管理）
```

**Skills 清单（评测 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `eval_standard_skill` | 查询评测标准（3GPP/TMForum/IEEE） | `get_eval_standard(nf_type="AMF", domain="security")` |
| `scenario_query_skill` | 查询评测场景库 | `query_eval_scenario(uc_type="intent-driven")` |
| `metric_query_skill` | 查询历史评测指标数据和基线 | `get_metric_baseline(kpi="intent_accuracy")` |
| `llm_judge_skill` | 使用 LLM 作为评判者评估输出质量 | `llm_evaluate(output, criteria, rubric)` |
| `regression_check_skill` | 回归检查（与历史基线对比） | `regression_check(new_results, baseline)` |

---

### 4.3 测试设计 Agent

#### 洞察

**主要功能**：测试策略设计、测试用例设计、测试场景生成、测试数据生成

**关键问题**：
- 如何自动生成覆盖电信协议所有分支的测试用例
- 如何设计 Agent 行为的测试策略（意图测试、状态机测试）

**业界优秀实践**：
- GitHub Copilot 测试生成：[https://github.blog/ai-and-ml/github-copilot/](https://github.blog/ai-and-ml/github-copilot/)
- Anthropic Cookbook（Claude 测试用例生成示例）：[https://github.com/anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook)

#### 测试设计 Agent Playground

**agent.md（测试设计 Agent）**：
```markdown
# 测试设计 Agent 能力范围
负责为 6G Core Agent NF 设计全面的测试方案。

## 能力范围
- 测试策略设计：基于风险和业务优先级制定测试策略
- 测试用例设计：覆盖功能/边界/异常/性能/安全多维度
- 测试数据生成：生成符合 3GPP 规范的测试数据

## 测试策略设计 Prompt
分析以下变更影响范围，设计测试策略：
1. 核心路径：必须覆盖（P0）
2. 影响范围：需要回归（P1）
3. 边界条件：需要专项（P2）
4. 风险区域：重点关注（P0+）

## 测试用例设计 Prompt
为以下功能生成测试用例，要求：
- 正常场景：至少 3 个典型用例
- 异常场景：覆盖所有错误分支
- 边界场景：空值/最大值/并发
- 性能场景：基准 TPS/时延测试
```

**soul.md（测试设计 Agent）**：
```markdown
# 测试设计规范（Test Design Agent Soul）
## 用例设计原则
- 等价类划分：每个等价类至少 1 个用例
- 边界值分析：所有边界必须覆盖
- 错误猜测：基于历史 Bug 库补充测试

## 6G 协议测试规范
- 遵循 3GPP TS 38 系列协议一致性测试规范
- 意图测试：覆盖 TMForum 意图 NBI 定义的所有意图类型
- 覆盖率要求：语句覆盖 > 85%，分支覆盖 > 80%
```

**Skills 清单（测试设计 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `scenario_lib_skill` | 查询测试场景库（3GPP/TMForum 场景） | `query_scenario(nf="AMF", flow="UE_Registration")` |
| `test_case_lib_skill` | 查询历史测试用例库（避免重复设计） | `find_existing_tests(feature="session_management")` |
| `test_strategy_skill` | 查询测试策略模板库 | `get_strategy_template(change_type="new_feature")` |
| `failure_analysis_skill` | 分析历史缺陷，补充测试用例 | `analyze_historical_bugs(module="AMF")` |
| `data_gen_skill` | 生成测试数据（3GPP 协议数据格式） | `gen_test_data(protocol="NAS", scenario="attach")` |

---

### 4.4 测试用例开发和执行 Agent

#### 洞察

**主要功能**：
- 将测试设计转化为可执行的测试代码
- 自动执行测试并收集结果
- 失败分析和缺陷报告生成

**关键问题**：
- AI 生成测试代码的可靠性（测试代码本身的质量）
- 大规模测试用例的并行执行调度
- 测试结果的智能分析（区分 AI 不稳定和真实 Bug）

**业界优秀实践**：
- LLM Self-Debug（LLM 自调试能力）：[https://arxiv.org/abs/2304.05128](https://arxiv.org/abs/2304.05128)
- open-swe 自动执行测试：[https://github.com/langchain-ai/open-swe](https://github.com/langchain-ai/open-swe)
- OpenAI Evals 执行框架：[https://github.com/openai/evals](https://github.com/openai/evals)

#### 测试用例开发和执行 Agent Playground

**agent.md（测试执行 Agent）**：
```markdown
# 测试用例开发和执行 Agent 能力范围
负责将测试设计转化为代码并执行。

## 能力范围
- 用例开发：将测试用例设计转化为可执行的测试脚本
- 用例执行：在测试环境中执行测试，收集结果
- 结果分析：分析失败用例，区分 AI 不稳定和真实 Bug
- 缺陷报告：自动生成缺陷报告，提交到缺陷管理系统

## 用例开发 Prompt
根据以下测试设计，生成测试代码：
- 使用框架：Go test（单元/集成）/ pytest（AI 功能）/ k6（性能）
- 严格遵循 soul.md 中的测试编码规范
- 每个用例必须包含：Setup / 执行步骤 / 验证 / Teardown

## 用例执行 Prompt
执行测试时：
1. 并行执行独立用例（最大并发度 = CPU 核数）
2. 失败用例自动重试 3 次（排除环境抖动）
3. 收集完整日志、覆盖率报告、性能数据
```

**soul.md（测试执行 Agent）**：
```markdown
# 测试编码和执行规范（Test Execution Agent Soul）
## 测试代码规范
- 测试代码与生产代码同等质量要求
- 禁止在测试中直接访问数据库（使用 Mock）
- 超时设置：单元测试 < 10s，集成测试 < 60s，E2E < 300s

## 测试执行约束
- 禁止在生产环境执行破坏性测试
- 性能测试必须在隔离环境中执行
- 测试完成后必须清理测试数据
```

**Skills 清单（测试执行 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `test_code_gen_skill` | 将测试设计转化为可执行测试代码 | `gen_test_code(test_design, framework="pytest")` |
| `test_exec_skill` | 执行测试（支持并行、超时控制） | `run_tests(test_suite, parallel=True, timeout=60)` |
| `coverage_collect_skill` | 收集代码覆盖率报告 | `collect_coverage(test_results)` |
| `failure_analysis_skill` | 分析测试失败原因（AI 不稳定 vs 真实 Bug） | `analyze_failure(failed_tests, retry_results)` |
| `bug_report_skill` | 自动生成并提交缺陷报告 | `create_bug_report(failure_info, severity="P1")` |


---

## 五、部署

### 洞察

#### 5.1.1 部署模式对比洞察

| 对比维度 | 传统云服务化部署模式 | Agent 化部署模式（Harness Engineering） | 关键差异说明 |
|---------|------------------|--------------------------------------|-----------|
| **部署规范** | YAML/Helm Chart 声明式配置 | agent.md + soul.md + YAML | 自然语言部署意图 + 技术配置 |
| **部署形态** | 容器（Docker）+ K8s | 容器 + Agent 容器 + GPU Pod + MicroVM 沙箱 | 新增 AI 推理容器和安全沙箱 |
| **部署体验** | CI/CD 流水线（Jenkins/GitOps） | 意图驱动部署（"将 AMF Agent 灰度发布到 Region A"） | 从配置式到意图式 |
| **部署技术** | Helm + ArgoCD/Flux + Kubernetes | Helm + ArgoCD/Flux + Agent 编排 + AI 验证 | 新增 AI 智能部署决策和验证 |

**优秀实践**：
- GitOps + Flux MCP（KubeCon EU 2026 实践）：[http://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759](http://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759)（演示 AI Agents 自动生成 GitOps 流水线）
- 华为 KubeCon EU 2026（跨集群 LLM 任务调度，Volcano Global + Karmada）：[http://kccnceu2026.sched.com/event/a100f382f331c59d59f1046a91411d71](http://kccnceu2026.sched.com/event/a100f382f331c59d59f1046a91411d71)
- Port IDP（5 分钟构建内部开发者门户）：[http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49](http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49)

---

#### 5.1.2 业务诉求洞察

**5GC vs 6G 部署差异**：

| 部署维度 | 5GC 部署 | 6G 部署 | 关键变化 |
|---------|---------|---------|---------|
| **部署对象** | 传统网元（AMF/SMF/UPF 等容器） | Agent NF + 传统微服务 + AI 推理服务 | 新增 GPU/NPU 推理 Pod 部署 |
| **部署频率** | 季度/月度大版本发布 | 持续交付（每天多次）、特性标志 | 需要零停机增量部署能力 |
| **部署验证** | 协议一致性测试（ICT）+ 基本功能测试 | 传统测试 + Agent 行为评测 + 意图验证 | 新增 AI 行为部署验证 |
| **部署环境** | 单一电信云（OpenStack/K8s） | 多云 + 边缘 + 端侧（云边端协同部署） | 云边端一体化部署编排 |
| **部署安全** | 网络隔离 + 镜像签名 | 网络隔离 + 镜像签名 + AI 推理沙箱 + 模型完整性验证 | 新增模型文件安全验证 |

**6G 部署关键技术挑战**：
1. **模型权重部署**：大模型（>10GB）的快速分发和热更新
2. **边缘部署**：资源受限边缘节点的 Agent 轻量化部署
3. **零停机升级**：Agent 升级时的状态迁移和上下文保存

---

#### 5.1.3 技术趋势洞察

**AI Native 部署技术演进**：
- vCluster 本地 K8s 与生产等价（减少 "Works on My Machine" 问题）：[http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd)
- AI 辅助的 GitOps：Flux MCP + Agent 自动化运维：[http://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759](http://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759)
- Dapr Agents 可靠部署（2 个月从概念到生产）：[http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd)

---

### 5.2 部署设计 Agent

#### 洞察

**主要功能**：部署策略设计、部署拓扑规划、灰度策略设计、回滚方案设计

**业界优秀实践**：
- Argo Rollouts（高级部署策略：蓝绿/金丝雀/渐进式）：[https://argoproj.github.io/rollouts/](https://argoproj.github.io/rollouts/)
- Flagger（基于 Prometheus 指标的自动化渐进式发布）：[https://flagger.app/](https://flagger.app/)

#### 部署设计 Agent Playground

**agent.md（部署设计 Agent）**：
```markdown
# 部署设计 Agent 能力范围
负责为 6G Core Agent NF 设计安全可靠的部署方案。

## 能力范围
- 部署策略设计：蓝绿/金丝雀/渐进式部署策略
- 资源规划：计算/存储/网络资源需求分析
- 灰度策略：流量比例、指标门禁、自动晋级条件
- 回滚方案：自动/手动回滚触发条件和执行步骤

## 部署策略设计 Prompt
根据以下应用特征，推荐最优部署策略：
- 服务类型：控制面（需要 0 停机）/ 用户面（可短暂中断）/ Agent（需要状态迁移）
- 变更风险：大版本（金丝雀）/ 小版本（滚动更新）/ 紧急修复（蓝绿切换）
```

**soul.md（部署设计 Agent）**：
```markdown
# 部署规范（Deploy Design Agent Soul）
## 部署策略原则
- 控制面网元：必须零停机部署（滚动更新或蓝绿）
- 用户面网元：允许计划内短暂中断（滚动更新，最大 unavailable=1）
- Agent NF：支持状态迁移的灰度部署

## 6G 电信级部署约束
- 生产变更：必须经过 UAT 环境验证
- 灰度流量：初始不超过 5%，每步晋级需观察 1 小时
- 回滚 RTO：< 5 分钟（自动触发）
- 关键业务：禁止在高峰时段（08:00-22:00）执行大版本升级
```

**Skills 清单（部署设计 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `deploy_scenario_skill` | 查询部署场景库（电信场景最佳实践） | `query_deploy_scenario(nf_type="AMF_Agent")` |
| `strategy_template_skill` | 查询部署策略模板 | `get_strategy_template(risk_level="high")` |
| `failure_analysis_skill` | 分析历史部署问题，优化策略 | `analyze_deploy_history(nf="SMF")` |
| `resource_calc_skill` | 计算资源需求（CPU/GPU/内存/存储） | `calc_resource(replicas=3, model_size="7B")` |

---

### 5.3 部署开发 Agent

#### 洞察

**主要功能**：Helm Chart 生成、CI/CD 流水线生成、部署脚本开发、基础设施即代码（IaC）生成

**业界优秀实践**：
- Helm（Kubernetes 应用包管理）：[https://helm.sh/](https://helm.sh/)
- Tekton（云原生 CI/CD 流水线）：[https://tekton.dev/](https://tekton.dev/)
- Terraform（基础设施即代码）：[https://www.terraform.io/](https://www.terraform.io/)

#### 部署开发 Agent Playground

**agent.md（部署开发 Agent）**：
```markdown
# 部署开发 Agent 能力范围
负责开发 6G Core Agent NF 的部署交付物。

## 能力范围
- Helm Chart 生成：根据部署设计自动生成 Helm Chart
- CI/CD 流水线：生成 GitHub Actions / Tekton 流水线
- 配置管理：生成环境变量、ConfigMap、Secret 管理方案
- IaC：生成 Terraform / Pulumi 基础设施代码

## 开发 Prompt
根据以下部署设计，生成部署代码：
1. 遵循 soul.md 中的部署开发规范
2. 所有敏感配置使用 Kubernetes Secret（禁止硬编码）
3. 为 Agent 组件配置 GPU 资源 limits 和 requests
4. 设置正确的 securityContext（非 root，只读文件系统）
```

**soul.md（部署开发 Agent）**：
```markdown
# 部署开发规范（Deploy Dev Agent Soul）
## 代码质量规范
- Helm Chart：values.yaml 必须有默认值和注释
- 镜像：必须指定固定版本（禁止 latest 标签）
- 资源：所有容器必须设置 resources.requests 和 resources.limits

## 安全规范
- 禁止在代码中明文存储任何密钥/密码
- 使用 Kubernetes Secrets 或外部 Vault（HashiCorp Vault）管理密钥
- 所有流水线步骤使用最小权限 ServiceAccount
```

**Skills 清单（部署开发 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `helm_gen_skill` | 生成 Helm Chart（支持 Agent NF 模板） | `gen_helm_chart(app_config, nf_type="agent")` |
| `pipeline_gen_skill` | 生成 CI/CD 流水线（GitHub Actions/Tekton） | `gen_pipeline(deploy_strategy="canary")` |
| `secret_mgmt_skill` | 生成密钥管理方案（K8s Secret / Vault） | `setup_secrets(secret_list, backend="vault")` |
| `iac_gen_skill` | 生成基础设施即代码（Terraform） | `gen_iac(infra_spec, provider="kubernetes")` |

---

### 5.4 部署执行 Agent

#### 洞察

**主要功能**：自动执行部署、监控部署进度、自动晋级/回滚、变更审批工作流

**关键问题**：
- 部署执行的幂等性保证（重复执行不产生副作用）
- 关键业务的人工审批流程集成（HITL）
- 部署过程中的实时可观测性

**业界优秀实践**：
- ArgoCD（GitOps 持续部署）：[https://argo-cd.readthedocs.io/en/stable/](https://argo-cd.readthedocs.io/en/stable/)
- Argo Rollouts（渐进式发布控制器）：[https://argoproj.github.io/rollouts/](https://argoproj.github.io/rollouts/)
- HolmesGPT（AI 驱动的 K8s 问题诊断）：[http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49](http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49)

#### 部署执行 Agent Playground

**agent.md（部署执行 Agent）**：
```markdown
# 部署执行 Agent 能力范围
负责安全可靠地执行 6G Core Agent NF 的部署操作。

## 能力范围
- 部署执行：通过 GitOps（ArgoCD/Flux）执行部署
- 进度监控：实时监控 Pod 状态、健康检查、就绪探针
- 自动决策：基于指标门禁自动晋级或触发回滚
- 变更审批：生产变更自动触发人工审批流程（HITL）

## 部署执行 Prompt
执行部署时严格遵循：
1. 先在非生产环境验证通过，再执行生产部署
2. 关键操作（生产变更）必须等待人工审批
3. 实时监控所有 Pod 状态和服务指标
4. 出现异常立即停止并评估是否回滚
```

**soul.md（部署执行 Agent）**：
```markdown
# 部署执行规范和约束（Deploy Exec Agent Soul）
## 执行权限约束
- 开发环境：Agent 可自主执行所有操作
- 测试环境：Agent 可自主执行，需要操作日志
- 生产环境：所有变更必须有工单和人工审批

## 安全约束
- 禁止在无审批的情况下修改生产配置
- 禁止删除含有用户数据的存储资源
- 所有操作必须记录审计日志（留存 90 天）

## 自动回滚触发条件
- 错误率 > 1%（持续 2 分钟）
- P99 时延 > SLA 阈值 150%（持续 5 分钟）
- Pod 重启次数 > 3（5 分钟内）
```

**Skills 清单（部署执行 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `argocd_sync_skill` | 通过 ArgoCD 同步应用（GitOps） | `argocd_sync(app="amf-agent", namespace="prod")` |
| `deploy_status_skill` | 查询部署状态（Pod/Service/Endpoint） | `get_deploy_status(deployment="amf-agent-v2")` |
| `hitl_approval_skill` | 触发人工审批流程 | `request_approval(change_desc, approver_list)` |
| `auto_rollback_skill` | 自动回滚到上一版本 | `rollback(deployment="amf-agent", reason="error_rate_high")` |
| `audit_log_skill` | 记录操作审计日志 | `audit_log(action="deploy", target, result)` |

---

### 5.5 部署拨测 Agent

#### 洞察

**主要功能**：部署后自动拨测验证、性能基线验证、业务功能验证、观测指标分析

**关键问题**：
- 拨测覆盖率：如何确保拨测覆盖所有关键业务路径
- 拨测速度：快速拨测（< 10min）vs 全量验证（可能数小时）的平衡
- 误报率控制：避免因环境抖动产生误报触发不必要回滚

**业界优秀实践**：
- KubeTrace（AI 驱动的 5G Core 故障诊断，Deutsche Telekom）：[http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd)
- k6（现代化负载测试工具）：[https://k6.io/](https://k6.io/)

#### 部署拨测 Agent Playground

**agent.md（拨测 Agent）**：
```markdown
# 拨测 Agent 能力范围
负责 6G Core Agent NF 部署后的自动验证。

## 能力范围
- 快速拨测（Smoke Test）：5 分钟内完成关键路径验证
- 全量拨测（Regression）：覆盖所有业务功能验证
- 性能拨测：验证时延、吞吐量是否满足 SLA
- 意图拨测（Agent 特有）：验证 Agent 意图理解准确率
```

**soul.md（拨测 Agent）**：
```markdown
# 拨测规范（Probe Agent Soul）
## 拨测分级
- L1（Smoke Test）：30 个核心用例，5 分钟完成，部署后立即执行
- L2（功能验证）：200 个用例，30 分钟完成，Smoke Test 通过后执行
- L3（全量回归）：1000+ 用例，2 小时完成，重大版本发布前执行

## 成功标准
- 核心接口成功率：> 99.9%
- P99 时延：< SLA 定义阈值
- Agent 意图准确率：> 95%（6G 场景要求）
```

**Skills 清单（拨测 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `probe_standard_skill` | 查询拨测标准（3GPP 协议要求） | `get_probe_standard(nf="AMF", scenario="registration")` |
| `scenario_lib_skill` | 查询拨测场景库，生成拨测用例 | `query_probe_scenarios(priority="P0", nf="AMF_Agent")` |
| `test_case_exec_skill` | 执行拨测用例 | `exec_probe(cases=smoke_cases, timeout=300)` |
| `metric_query_skill` | 查询并分析观测指标（Prometheus/Grafana） | `query_metrics(service="amf-agent", period="5m")` |
| `report_gen_skill` | 生成拨测报告（通过率/性能/风险点） | `gen_probe_report(results, baseline)` |


---

## 六、运行

### 洞察

#### 6.1.1 运行模式对比洞察

| 对比维度 | 传统云服务化运行模式 | Agent 智能化 Harness 运行模式 | 关键差异 |
|---------|------------------|------------------------------|---------|
| **异构计算** | 纯 CPU 微服务 | CPU + GPU/NPU 混合（AI 推理） | 新增 GPU/NPU 资源调度和隔离 |
| **分布式** | 微服务分布式（Service Mesh） | 微服务 + Agent 分布式编排（LangGraph） | 新增 Agent 协作的分布式状态管理 |
| **并行** | 并发请求处理（线程池） | 并行 Agent 执行 + 并行 Token 推理 | 推理并行是新的并发维度 |
| **运行环境** | 容器（Docker/K8s） | 容器 + Agent Loop + MicroVM 沙箱 | 新增 AI 推理运行时和安全沙箱 |
| **安全** | 网络隔离 + RBAC | 网络隔离 + RBAC + Sandbox + AI 审计 | AI 生成代码需要安全隔离执行 |
| **性能** | CPU 指标（QPS/时延） | CPU + GPU 利用率 + Token 吞吐 + 推理时延 | 新增 AI 特有性能指标 |

**优秀实践**：
- Ray（异构分布式 AI 运行时）：[https://github.com/ray-project/ray](https://github.com/ray-project/ray)
- vLLM（高性能 LLM 推理引擎，PagedAttention 技术）：[https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
- Kubernetes Agent Sandbox：[https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/)

---

#### 6.1.2 业务诉求洞察

| 运行维度 | 5GC 运行 | 6G 运行 | 关键变化 |
|---------|---------|---------|---------|
| **运行时形态** | 标准容器（CPU only） | 容器 + GPU Pod + Edge Agent | 多形态混合部署 |
| **资源占用** | 确定性资源（CPU/Memory） | 动态资源（GPU 按需分配）| GPU 资源弹性伸缩 |
| **性能规格** | 固定 TPS 规格（线性伸缩） | 变长推理（Token 数影响时延）| 需要 KV Cache 管理和批处理优化 |
| **分布式能力** | Service Mesh（Istio） | Service Mesh + Agent 编排 + ACN | 新增 Agent 级别分布式协调 |
| **安全** | mTLS + RBAC | mTLS + RBAC + 推理沙箱 + 模型完整性 | AI 推理安全成为新约束 |

---

#### 6.1.3 技术趋势洞察

**AI 生成代码如何安全高效运行**：
- MicroVM 沙箱（Firecracker）提供毫秒级启动的安全隔离：[https://github.com/firecracker-microvm/firecracker](https://github.com/firecracker-microvm/firecracker)
- AI 与人工代码共存策略：AI 处理业务逻辑，人工框架代码提供可靠性兜底（参考：[https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)）
- 运行时行为验证：通过 eBPF 监控 AI 生成代码的系统调用行为：[https://ebpf.io/](https://ebpf.io/)

---

### 6.2 Agent 运行时

#### 洞察

**业界定义**：Agent 运行时是提供 Agent 生命周期管理、执行编排、上下文管理和 Skills 调度的中间件层，是 Harness Engineering 的核心基础设施。

**主要组件**：
- **Agent 编排**：基于 LangGraph/ADK 的工作流图执行引擎
- **上下文管理**：RAG 检索 + 历史压缩 + 动态 Prompt 管理
- **Skills 调度**：MCP 工具调用路由、权限控制、结果缓存
- **评估引擎**：Eval Loop 自动评估 Agent 输出质量
- **沙箱执行**：隔离的代码执行环境（MicroVM/容器沙箱）

**竞争力构筑**：精度（Accuracy）+ 确定性（Determinism）+ 端到端时延（E2E Latency）

**关键技术突破**：
1. 上下文压缩：将 200K Token 上下文压缩到 10K 以内而不丢失关键信息
2. Skills 热加载：新 Skill 注册后无需重启 Agent
3. Eval Loop 闭环：自动检测 Agent 输出质量退化

**业界优秀实践**：
- LangGraph 生产级 Agent 运行时（Klarna/Replit/Elastic 部署）：[https://github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- DeepAgents（内置全套 Harness 的 Agent 运行时）：[https://github.com/langchain-ai/deepagents](https://github.com/langchain-ai/deepagents)
- Deer-Flow（ByteDance，荣登 GitHub Trending 第一）：[https://github.com/bytedance/deer-flow](https://github.com/bytedance/deer-flow)
- OpenAI Agents SDK（生产级 Harness 框架）：[https://github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python)
- Darwin Gödel Machine（Agent 运行时自进化，SWE-bench 提升 150%）：[https://arxiv.org/abs/2505.22954](https://arxiv.org/abs/2505.22954)

#### Agent 运行时 Playground

**关键诉求和命题**：

| 命题 | 当前挑战 | 突破方向 |
|------|---------|---------|
| 精度保障 | Agent 输出质量不稳定，幻觉率高 | Eval Loop 自动检测 + Guardrails 拦截 |
| 确定性 | 相同任务多次执行结果不一致 | 温度控制 + 输出格式约束 + 结果缓存 |
| 端到端时延 | 多轮 Agent 调用累积时延过高 | 并行工具调用 + 上下文缓存 + 流式输出 |
| 上下文溢出 | 长任务超出 Token 窗口限制 | 层次化记忆 + 选择性压缩 + 外部记忆 |
| Skills 安全 | Skills 权限过大，存在安全风险 | 最小权限 + MCP 授权 + Sandbox 隔离 |

---

### 6.3 模型运行时

#### 洞察

**业界定义**：模型运行时是专为 LLM 推理设计的高性能执行引擎，核心目标是最大化 GPU 利用率、最小化推理时延、降低单 Token 成本。

**主要组件**：
- **推理框架**：vLLM/SGLang（高性能推理，PagedAttention/RadixAttention）
- **算子算法加速**：FlashAttention、算子融合、INT4/INT8 量化
- **分布式推理**：Tensor Parallelism + Pipeline Parallelism + Expert Parallelism（MoE）
- **Prefill-Decode 分离**：Dynamo/llm-d（分离式调度，提升吞吐）

**竞争力构筑**：推理吞吐（Tokens/s）+ 首 Token 时延（TTFT）+ 单 Token 成本

**技术突破方向**：
1. 推理吞吐：PagedAttention（vLLM）实现 GPU 显存零碎片，吞吐提升 24x
2. 时延优化：Speculative Decoding 将生成速度提升 3x
3. 成本降低：量化（INT4）将显存需求降低 4x，降低部署成本

**业界优秀实践**：
- vLLM（高性能 LLM 推理，PagedAttention，主流推理框架）：[https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
- SGLang（结构化 LLM 生成，RadixAttention，KV Cache 重用）：[https://github.com/sgl-project/sglang](https://github.com/sgl-project/sglang)
- llm-d（跨集群分布式推理，IBM/Red Hat，KubeCon EU 2026）：[http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd)
- TensorRT-LLM（NVIDIA 算子加速）：[https://github.com/NVIDIA/TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)

#### 模型运行时 Playground

**关键诉求和命题**：

| 命题 | 指标目标 | 当前挑战 | 突破方向 |
|------|---------|---------|---------|
| 推理吞吐 | >10K Tokens/s（70B 模型） | GPU 利用率低（<50%） | PagedAttention + Continuous Batching |
| 首 Token 时延（TTFT） | <500ms（交互式场景） | Prefill 计算密集，阻塞 Decode | Prefill-Decode 分离（Dynamo） |
| 单 Token 成本 | 持续降低（目标：千 Token<¥0.01） | 大模型部署成本高 | 量化 + 蒸馏 + 共享 KV Cache |
| 长上下文推理 | 支持 200K+ Token（6G 复杂场景） | 显存线性增长 | 滑动窗口注意力 + 外部 KV Cache |
| 多模型并发 | 同一 GPU 运行多个模型实例 | GPU 显存竞争 | 时分复用 + 模型权重共享 |

---

### 6.4 治理 Agent

#### 洞察

**主要功能**：
- Agent 服务注册发现和健康管理
- 流量控制（限流、熔断、负载均衡）
- 合规审计（Agent 操作审计、数据使用审计）
- 容量管理（GPU 资源调度、模型实例伸缩）

**关键问题**：
- Agent 服务治理与传统微服务治理的差异（非确定性服务的治理）
- 跨 Agent 调用的分布式追踪（LLM 调用的追踪）
- Agent 异常行为的快速发现和隔离

**业界优秀实践**：
- Istio（Service Mesh 治理，流量控制/可观测性）：[https://istio.io/](https://istio.io/)
- agentgateway（MCP 数据面 + Kyverno 策略，KubeCon EU 2026）：[http://kccnceu2026.sched.com/event/7894a8a1796a190531bbdbe9379d681a](http://kccnceu2026.sched.com/event/7894a8a1796a190531bbdbe9379d681a)
- HolmesGPT（AI 驱动 K8s 故障诊断，CNCF Sandbox）：[http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49](http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49)
- Keycloak MCP 授权（企业级 MCP 安全）：[http://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759](http://kccnceu2026.sched.com/event/90de8b6bc1b399b4e26695f426537759)

#### 治理 Agent Playground

**agent.md（治理 Agent）**：
```markdown
# 治理 Agent 能力范围
负责 6G Core AI Native 平台中所有 Agent 和模型推理服务的治理。

## 能力范围
- 服务发现：查询和管理已注册的 Agent NF 实例
- 健康管理：监控 Agent 健康状态，自动重启异常实例
- 流量控制：执行限流、熔断、灰度路由策略
- 合规审计：记录和分析 Agent 操作审计日志
- 容量管理：根据负载自动调整 Agent 副本数和 GPU 资源分配
```

**soul.md（治理 Agent）**：
```markdown
# 治理规范（Governance Agent Soul）
## 治理原则
- 最小干预：优先自动修复，无法自动修复才升级人工
- 审计完整性：所有 Agent 操作必须有完整审计记录
- 安全优先：发现安全风险立即隔离，后续人工确认

## 合规约束
- 用户数据访问：必须有授权记录，日志留存 >= 90 天
- 跨境数据：遵循数据主权要求，禁止非授权跨境传输
- AI 决策：重大业务决策必须有人工审批记录
```

**Skills 清单（治理 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `agent_registry_skill` | 查询 Agent 注册信息（名称/版本/状态/端点） | `list_agents(namespace="6g-core", status="running")` |
| `health_monitor_skill` | 查询 Agent 健康状态和历史指标 | `get_health(agent="amf-agent", period="1h")` |
| `traffic_control_skill` | 执行流量控制策略（限流/熔断/路由） | `apply_rate_limit(agent="smf-agent", rps=1000)` |
| `audit_query_skill` | 查询 Agent 操作审计日志 | `query_audit(agent="system-agent", action="intent_process")` |
| `scale_skill` | 自动伸缩 Agent 实例（HPA/VPA） | `scale_agent(agent="amf-agent", target_replicas=5)` |


---

## 七、运维

### 洞察

#### 7.1.1 运维模式对比洞察

| 对比维度 | 传统云服务化运维模式 | Agent 智能化运维模式 | 关键差异 |
|---------|------------------|------------------|---------|
| **OM UI 交互** | Web 控制台（表单/图表/配置页） | 意图驱动 UI（自然语言 + AI 生成界面） | 从"配置式"到"对话式"运维 |
| **运维对象** | 容器/虚机/网络/存储（基础设施） | 基础设施 + Agent NF + 模型推理服务 | 新增 AI 推理服务和 Agent 的运维对象 |
| **运维场景** | 告警响应/容量规划/变更管理 | 意图驱动运维/自主故障诊断/AI 辅助配置 | 从被动响应到主动自愈 |
| **运维指标** | CPU/内存/网络/时延/错误率 | 传统指标 + Token 吞吐/推理时延/意图准确率/Agent 精度 | 新增 AI 特有 KPI |
| **关键技术** | Prometheus/Grafana/ELK/PagerDuty | OTel + LLM Tracing + AI 故障诊断 + 意图运维 | 全栈 AI 增强运维能力 |

**优秀实践**：
- KubeTrace（Deutsche Telekom，AI 自主关联诊断 5G Core 故障，秒级）：[http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd)
- HolmesGPT（CNCF Sandbox，LLM 连接运维数据自动诊断修复）：[http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49](http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49)
- Agentic GitOps（ControlPlane，MCP enabled AI 辅助运维）：[http://kccnceu2026.sched.com/event/55bd23423789cd1d328edf6bb67f770d](http://kccnceu2026.sched.com/event/55bd23423789cd1d328edf6bb67f770d)

---

#### 7.1.2 业务诉求洞察

**5GC vs 6G 运维差异**：

| 运维维度 | 5GC 运维 | 6G 运维 | 关键变化 |
|---------|---------|---------|---------|
| **运维交互** | Web 管理界面（EMS/NMS） | 自然语言意图运维 + AI 生成 Web UI | 从表单配置到自然语言对话 |
| **运维对象** | AMF/SMF/UPF 等传统网元 | 传统网元 + Agent NF + 意图引擎 + 模型推理 | 新增 AI 服务运维对象 |
| **告警处理** | 人工响应（MTTR 小时级） | Agent 自主诊断修复（MTTR 分钟级） | 自愈能力成为核心竞争力 |
| **配置管理** | NETCONF/YANG 模型配置 | 意图驱动配置（"将 Region A 的 QoS 策略调整为 XR 优先"） | 意图驱动配置替代手工配置 |
| **容量规划** | 基于历史数据的静态规划 | AI 预测 + 动态资源调整 | AI 驱动的弹性容量管理 |

---

#### 7.1.3 技术趋势洞察

**AI 生成 Web 运维界面**：
- AI 根据运维意图动态生成数据看板和操作界面（参考 Port IDP 实践：[http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49](http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49)）
- 意图驱动数据查询：自然语言查询替代复杂 PromQL/SQL（参考 NL2SQL 技术）

**AI 辅助运维可靠性保障**：
- AI 运维操作必须有安全约束（soul.md 定义禁止操作列表）
- 人工审批 HITL（关键操作：生产配置变更必须有人工确认）
- AI 生成运维代码安全隔离执行（Sandbox）
- 人工编写可靠性框架为 AI 运维代码兜底（熔断/回滚/超时）

参考：
- 电信 Agentic AI 自主网络（Orange/Linux Foundation，KubeCon EU 2026）：[http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd)
- AI 意图驱动运维（TMForum）：[https://www.tmforum.org/intent-nbi/](https://www.tmforum.org/intent-nbi/)

---

### 7.2 运维 Agent

#### 洞察

**主要功能**：
- 意图理解：将运维人员的自然语言意图转化为具体运维操作
- 故障诊断：自主分析告警、关联日志/指标，给出根因分析
- 自动修复：在授权范围内自动执行修复操作（重启/扩容/配置回滚）
- 配置管理：基于意图自动生成和验证配置变更
- 容量规划：基于 AI 预测自动调整资源分配

**关键问题**：
- 运维操作的安全边界（哪些操作 Agent 可以自主执行，哪些需要人工审批）
- AI 故障诊断的准确性（减少误判，避免误操作）
- 多系统数据关联（日志/指标/告警/配置的综合分析）

**技术挑战**：
- 大规模电信网络的实时数据分析（百万级指标、TB 级日志）
- 运维操作的幂等性和安全性保障
- 跨域故障根因定位（无线 → 传输 → 核心网的端到端分析）

**业界优秀实践**：
- KubeTrace（Deutsche Telekom，AI 秒级诊断 5G Core 故障）：[http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd)
- HolmesGPT（CNCF Sandbox，K8s 自动故障诊断修复）：[http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49](http://kccnceu2026.sched.com/event/1ff722e8bc50da45979d6969e0503a49)
- Autonomous Telco（Deutsche Telekom，AI Agents 作为云原生基础设施一等公民）：[http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd](http://kccnceu2026.sched.com/event/fd10d8cf0054aac8f3206ddd6d996ccd)
- Telco Agentic AI（Orange + Linux Foundation，从 Cloud-Native 到 Agentic-AI-Native）：[http://kccnceu2026.sched.com/event/55bd23423789cd1d328edf6bb67f770d](http://kccnceu2026.sched.com/event/55bd23423789cd1d328edf6bb67f770d)

#### 运维 Agent Playground

**agent.md（运维 Agent）**：
```markdown
# 运维 Agent 能力范围
负责 6G Core AI Native 平台的智能运维。

## 能力范围
- 意图运维：理解运维人员自然语言意图，转化为操作步骤
- 故障诊断：自主分析告警/日志/指标，给出根因分析和修复建议
- 自动修复：在授权范围内自动执行修复操作（含安全约束）
- 配置管理：基于意图生成配置变更，验证后执行
- 容量规划：AI 预测负载趋势，提前规划资源扩容

## 意图运维 Prompt
接收运维意图，执行以下步骤：
1. 理解意图，确认操作范围和影响
2. 检查 soul.md 约束，评估操作风险
3. 高风险操作：请求人工审批（HITL）
4. 低风险操作：直接执行，记录审计日志
5. 执行后验证操作效果，报告结果

## 故障诊断 Prompt
收到告警后：
1. 收集相关上下文（告警详情/最近日志/指标趋势/最近变更）
2. 关联分析，识别根因（排除误报）
3. 查询故障模式库，匹配历史案例
4. 给出根因分析报告和修复建议
5. 高置信度（>90%）时自动执行修复，否则上报人工
```

**soul.md（运维 Agent）**：
```markdown
# 运维规范（Operations Agent Soul）
## 核心运维原则
- 安全第一：不确定时不操作，宁可升级人工
- 最小变更：只做必要的修复，不做多余操作
- 可逆操作：所有自动操作必须有回滚方案

## 自动执行授权范围（无需人工审批）
- Pod 重启（非核心业务）
- 自动扩容（增加副本，上限 2x）
- 非紧急告警的配置微调
- 日志级别临时调整

## 必须人工审批的操作
- 生产数据库的任何写操作
- 减少副本数（可能导致容量下降）
- 核心业务网元的配置变更
- 跨域配置同步

## 禁止操作
- 禁止在业务高峰期（08:00-22:00）执行影响用户的操作
- 禁止删除含用户数据的存储资源
- 禁止修改安全策略（RBAC/网络策略）

## 合规要求
- 所有操作必须记录审计日志
- 涉及用户数据的操作需要合规审批
- 审计日志留存 >= 90 天
```

**Skills 清单（运维 Agent）**：

| Skill | 功能 | 调用示例 |
|-------|------|---------|
| `ui_gen_skill` | 按意图生成运维数据看板/操作界面 | `gen_dashboard(intent="查看 AMF Agent 的推理性能趋势")` |
| `agent_query_skill` | 查询 Agent NF 运行状态、配置、历史 | `query_agent(name="amf-agent", fields=["status","metrics"])` |
| `metric_query_skill` | 查询运维指标数据（Prometheus/VictoriaMetrics） | `query_metric(expr="rate(amf_errors[5m])", period="1h")` |
| `log_query_skill` | 查询日志（Loki/ELK），支持自然语言查询 | `query_log(service="smf-agent", intent="查找最近的错误")` |
| `alert_query_skill` | 查询告警（AlertManager），关联分析 | `query_alerts(severity="critical", since="30m")` |
| `fault_pattern_skill` | 查询故障模式库，匹配历史案例 | `match_fault_pattern(symptoms=["high_error_rate","timeout"])` |
| `config_change_skill` | 执行配置变更（NETCONF/K8s ConfigMap） | `apply_config(target="amf-agent", config_patch, approval_id)` |
| `scale_skill` | 执行扩缩容操作 | `scale(deployment="smf-agent", replicas=5, reason="高负载")` |
| `restart_skill` | 重启 Agent 实例 | `restart_pod(pod_name="amf-agent-xyz", reason="内存泄漏")` |
| `audit_log_skill` | 记录操作审计日志 | `audit_log(operation, target, result, operator="ops-agent")` |

---

## 附录：参考文献总览

本文档所有引用链接均指向具体技术文章，按主题分类如下：

### Harness Engineering 核心
- OpenAI Harness Engineering 定义：[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)
- Martin Fowler Harness Engineering：[https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- LangChain Harness Engineering 实践：[https://blog.langchain.com/improving-deep-agents-with-harness-engineering/](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/)

### 6G 标准参考
- 3GPP 6G 用例：[https://www.3gpp.org/ftp/Specs/archive/22_series/22.847/](https://www.3gpp.org/ftp/Specs/archive/22_series/22.847/)
- ITU IMT-2030：[https://www.itu.int/rec/R-REC-M.2160/en](https://www.itu.int/rec/R-REC-M.2160/en)
- ETSI 6G：[https://www.etsi.org/technologies/6g](https://www.etsi.org/technologies/6g)

### AI Native 平台
- CNCF Cloud Native 定义：[https://github.com/cncf/toc/blob/main/DEFINITION.md](https://github.com/cncf/toc/blob/main/DEFINITION.md)
- KubeCon EU 2026 议程：[https://kccnceu2026.sched.com](https://kccnceu2026.sched.com)
- Kubernetes Agent Sandbox：[https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/)

### 关键开源项目
- LangGraph：[https://github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- DeepAgents：[https://github.com/langchain-ai/deepagents](https://github.com/langchain-ai/deepagents)
- vLLM：[https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
- MCP 协议：[https://github.com/modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol)
- OpenAI Agents SDK：[https://github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python)

