# 附录G：新名词与新技术术语表

本附录汇总了 Claude Code 及相关 AI 编程领域中出现的新名词、新技术和新概念，帮助读者快速理解这些术语的含义和背景。

---

## A

### Agent（智能体）

在 AI 领域，Agent 指具备自主决策和行动能力的 AI 系统。与传统的"问答式"AI 不同，Agent 能够：
- 自主规划任务步骤
- 调用外部工具完成任务
- 根据反馈调整行为
- 长时间自主工作

**Claude Code 中的应用**：Claude Code 本身就是一个 Agentic Coding Tool，能够自主分析代码、执行命令、修改文件。

### Agentic Coding Tool（智能编程工具）

指具备 Agent 能力的编程辅助工具，能够自主完成复杂的编程任务，而非仅响应单次查询。Claude Code 是 Anthropic 官方的 Agentic Coding Tool。

### Alignment（对齐）

AI 安全领域的核心概念，指确保 AI 系统的行为与人类意图和价值观一致。Anthropic 在这一领域有深入研究，Claude Sonnet 4.5 被称为"Anthropic 对齐性最好的模型"。

### Anthropic

Claude 模型和 Claude Code 的开发公司，成立于 2021 年，专注于 AI 安全研究。2025年11月完成 130 亿美元 F 轮融资，估值 1830 亿美元。

### API Key（API 密钥）

用于认证和授权 API 访问的密钥字符串。Anthropic API Key 通常以 `sk-ant-api03-` 开头。

### Artifacts

Claude 3.5 引入的功能，允许在对话中创建和展示可交互的内容（如代码、图表、游戏等）。

---

## C

### Claude

Anthropic 开发的大语言模型系列，以安全性和有用性著称。

### Claude Agent SDK

2025年9月随 Claude Sonnet 4.5 发布的软件开发工具包，用于构建基于 Claude 的自定义智能体应用。

```python
from anthropic import Agent, Tool

agent = Agent(
    model="claude-sonnet-4-5-20250929",
    tools=[...],
    system_prompt="..."
)
result = agent.run("完成任务...")
```

### Claude Code

Anthropic 官方推出的智能编程工具（Agentic Coding Tool），通过 npm 包 `@anthropic-ai/claude-code` 分发。能够在终端中运行，理解代码库，通过自然语言命令帮助开发者编写代码。

**官方安装方式**：
```bash
# 一键安装（推荐）
curl -fsSL https://claude.ai/install.sh | bash

# Homebrew
brew install claude-code

# npm
npm install -g @anthropic-ai/claude-code
```

### Claude Code on the Web

Claude Code 的网页版本，可通过浏览器直接使用，无需安装。访问地址：https://code.claude.com

### Claude Code for VS Code（Beta）

Claude Code 的 Visual Studio Code 扩展，提供图形化界面，可在 IDE 侧边栏直接使用 Claude，无需熟悉终端操作。

### Claude Code GitHub Actions

Claude Code 与 GitHub 的集成功能，允许在 PR 和 Issue 中通过 `@claude` 提及触发 AI 辅助，实现自动代码审查、功能实现、Bug 修复。

### Claude Code GitLab CI/CD

Claude Code 与 GitLab 的集成功能，支持在 GitLab CI/CD 流水线中使用 Claude Code 进行自动化任务。

### CLAUDE.md

Claude Code 的项目级配置文件，用于定义项目特定的规则、上下文和行为。类似于其他工具中的 `.cursorrules` 或 `.github/copilot`。

### Computer Use（计算机使用）

Claude 3.5 引入的能力，允许 AI 操作计算机界面，包括：
- 屏幕截图分析
- 鼠标和键盘操作
- GUI 自动化

Claude 4.5 系列在此能力上有重大提升。

### Constitutional AI（宪法 AI）

Anthropic 提出的 AI 训练方法，通过让 AI 根据一组预定义的原则进行自我批评和修正，减少有害输出，而非完全依赖人类反馈。

### Context Window（上下文窗口）

模型能够处理的最大输入长度，以 token 为单位。Claude 4.5 系列的上下文窗口为 200K tokens。

---

## F

### Function Calling（函数调用）

LLM 的一种能力，允许模型在对话中调用预定义的函数/工具。这是 Agent 能力的基础。Claude Code 的工具系统就是基于此能力构建的。

---

## H

### Haiku

Claude 模型系列中的轻量版本，特点是快速响应、低成本。

### Hooks（钩子）

Claude Code 的扩展机制，允许用户在特定事件点注入自定义逻辑：
- **PreToolUse**：工具调用前触发
- **PostToolUse**：工具调用后触发
- **Notification**：通知事件触发
- **Stop**：会话结束时触发

---

## I

### Interpretability（可解释性）

AI 安全领域的研究方向，致力于理解大语言模型内部的工作机制，使 AI 的决策过程更加透明。Anthropic 在此领域有深入研究。

---

## J

### JetBrains IDE Integration

Claude Code 与 JetBrains 系列 IDE（IntelliJ IDEA、PyCharm、WebStorm 等）的集成支持。

---

## L

### LLM（Large Language Model，大语言模型）

基于深度学习的语言模型，通过大规模文本数据训练，具备理解和生成自然语言的能力。Claude 是 LLM 的代表之一。

### LLM Gateway Configuration

企业级功能，允许配置 LLM 网关，用于流量管理、成本控制和安全审计。

---

## M

### MCP（Model Context Protocol，模型上下文协议）

Anthropic 于 2024年11月推出的开源协议，旨在标准化 AI 模型与外部数据源、工具之间的交互。可以理解为\"AI 世界的 USB 接口\"。

**核心组件**：
- **MCP Host**：运行 AI 模型的应用程序（如 Claude Code）
- **MCP Client**：AI 模型内部与 MCP 服务器通信的组件
- **MCP Server**：连接 AI 模型与外部系统的中间层

**2025年7月更新**：支持远程 MCP 服务器，无需本地部署。

**官方网站**：https://modelcontextprotocol.io

### MCP Connectors

MCP 连接器，用于连接各种外部服务和数据源，如 Google Drive、Figma、Jira、Slack 等。

### Memory System（记忆系统）

Claude Code 的功能，允许在会话之间保持信息，包括：
- 项目上下文记忆
- 用户偏好记忆
- 历史操作记忆

通过 `/memory` 命令管理。

### Multimodal（多模态）

指 AI 模型能够处理多种类型的输入（如文本、图像、音频、视频）。Claude 3.5 及以后版本支持图像输入。

---

## O

### OAuth

开放授权协议，Claude Code 使用 OAuth 实现与 Claude.ai 账户的认证。这是推荐的认证方式。

### Opus

Claude 模型系列中的旗舰版本，具备最强能力，常用于处理复杂编码和智能体任务。

---

## P

### Prompt Engineering（提示词工程）

设计和优化输入提示以获得更好 AI 输出的技术和方法论。在 Claude Code 中，良好的提示词设计能显著提升代码生成质量。

### Prompt Caching（提示缓存）

Claude API 的功能，允许缓存频繁使用的提示内容，降低重复请求的成本。定价分为写入和读取两部分。

### Plugins（插件）

Claude Code 的扩展机制，允许添加自定义功能和工具。与 Skills 类似但更底层。

---

## R

### RAG（Retrieval-Augmented Generation，检索增强生成）

一种结合信息检索和文本生成的技术，让 AI 能够基于外部知识库生成更准确的回答。MCP 协议支持 RAG 场景。

---

## S

### Scalable Oversight（可扩展监督）

AI 安全研究方向，研究如何在 AI 能力不断增强的情况下，保持人类对 AI 的有效监督。

### Skills（技能）

Claude Code 的能力扩展系统，允许封装和复用特定领域的知识和工具：
- **官方 Skills**：Anthropic 提供的通用能力
- **社区 Skills**：社区贡献的特定框架/语言支持
- **自定义 Skills**：用户自行开发的能力包

### Sonnet

Claude 模型系列中的均衡版本，在性能和成本之间取得平衡。

### Spec（规范）

Claude Code 的功能，支持规范驱动的开发模式：
- 解析需求文档
- 自动任务分解
- 进度跟踪
- 验证实现是否符合规范

---

## T

### Token

LLM 处理文本的基本单位，大致相当于 3-4 个英文字符或 1-2 个中文字符。Claude 4.5 系列支持 200K tokens 的上下文窗口。

### Tool Use（工具使用）

LLM 调用外部工具完成任务的能力。Claude Code 内置多种工具：
- **Read**：读取文件
- **Write**：写入文件
- **Edit**：编辑文件
- **Bash**：执行命令
- **Grep**：搜索内容
- **Glob**：文件匹配

---

## W

### WSL2（Windows Subsystem for Linux 2）

Windows 上运行 Linux 环境的技术。Claude Code 在 Windows 上必须通过 WSL2 运行。

### Web Search（网页搜索）

Claude 的功能，允许在对话中搜索网页获取最新信息。API 定价为 $10/千次搜索。

---

## 版本号命名规则

Claude 模型的版本号遵循以下规则：

| 格式 | 示例 | 说明 |
|------|------|------|
| claude-{tier}-{version}-{date} | claude-sonnet-4-5-20250929 | 完整 API 标识符 |
| Claude {Tier} {Version} | Claude Sonnet 4.5 | 市场名称 |

**Tier（层级）**：
- Opus：旗舰版，最强能力
- Sonnet：均衡版，性能与成本平衡
- Haiku：轻量版，快速低成本

**Version（版本）**：
- 4.5：2025年9-11月发布的最新系列
- 4：2025年5月发布
- 3.5：2024年6-10月发布
- 3：2024年3月发布

---

## 技术演进时间线

| 时间 | 技术/概念 | 说明 |
|------|----------|------|
| 2021年 | Anthropic 成立 | AI 安全公司创立 |
| 2023年3月 | Claude 1.0 | 首个公开版本 |
| 2023年7月 | Claude 2 | 100K 上下文 |
| 2024年3月 | Claude 3 系列 | Opus/Sonnet/Haiku 三层架构 |
| 2024年6月 | Claude 3.5 Sonnet | 代码能力飞跃 |
| 2024年10月 | Computer Use | 计算机操作能力 |
| 2024年11月 | MCP 协议 | 模型上下文协议发布 |
| 2025年5月 | Claude 4 系列 | 7小时连续工作 |
| 2025年7月 | 远程 MCP | 支持远程服务器 |
| 2025年9月 | Claude Sonnet 4.5 | Agent SDK 发布 |
| 2025年10月 | Claude Haiku 4.5 | 极速轻量版 |
| 2025年11月 | Claude Opus 4.5 | 旗舰级编码/智能体模型 |

---

## 相关工具对比术语

| 术语 | Claude Code 对应 | 其他工具对应 |
|------|-----------------|-------------|
| 配置文件 | CLAUDE.md | .cursorrules, .github/copilot |
| 扩展机制 | Skills, Hooks, MCP | Extensions, Plugins |
| Agent 模式 | 原生支持 | Cursor Composer, Windsurf Cascade |
| 命令行工具 | claude | aider, copilot-cli |

---

本术语表将随着技术发展持续更新。如有疑问或建议，欢迎反馈。
