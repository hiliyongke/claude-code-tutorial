# 附录 E：术语表

本附录提供 Claude Code 相关术语的定义和解释。

## E.1 核心概念

### Claude Code
Anthropic 公司开发的命令行 AI 编程助手，允许开发者在终端中与 Claude 模型交互。

### Claude
Anthropic 公司开发的大型语言模型系列，包括 Opus、Sonnet、Haiku 等不同版本。

### Token
语言模型处理文本的基本单位。一个 Token 大约相当于 4 个英文字符或 1-2 个中文字符。

### 上下文窗口（Context Window）
模型一次能够处理的最大 Token 数量。Claude 3 系列模型支持 200K Token 的上下文窗口。

### 提示词（Prompt）
发送给模型的输入文本，包括指令、问题或需要处理的内容。

## E.2 功能术语

### Tools
Claude Code 中的工具系统，允许模型执行特定操作，如读写文件、执行命令等。

### MCP（Model Context Protocol）
模型上下文协议，一种标准化的协议，用于扩展 Claude Code 的能力，连接外部服务和数据源。

### MCP Server
实现 MCP 协议的服务端程序，为 Claude Code 提供额外的工具和数据访问能力。

### Hooks
钩子机制，允许在特定事件（如会话开始、工具调用）发生时自动执行自定义脚本。

### Skills
技能系统，可复用的提示词模板和指令集，用于特定类型的任务。

### Spec
规范文档，用于描述开发任务的详细需求，支持规范驱动的开发方式。

### CLAUDE.md
项目配置文件，用于定义项目特定的规范、约束和上下文信息。

## E.3 模型术语

### Claude 3 Opus
Claude 3 系列中最强大的模型，适合复杂推理和高质量内容生成。

### Claude 3 Sonnet
Claude 3 系列中的平衡型模型，在性能和成本之间取得良好平衡。

### Claude 3 Haiku
Claude 3 系列中最快速、最经济的模型，适合简单任务。

### 推理（Inference）
模型根据输入生成输出的过程。

### 微调（Fine-tuning）
在预训练模型基础上，使用特定数据进一步训练以适应特定任务。

## E.4 技术术语

### API（Application Programming Interface）
应用程序编程接口，Claude Code 通过 Anthropic API 与模型通信。

### API Key
访问 API 的身份凭证，用于认证和计费。

### 流式输出（Streaming）
模型生成内容时逐步返回结果，而非等待完整响应。

### 上下文（Context）
提供给模型的背景信息，包括对话历史、文件内容、项目配置等。

### 幻觉（Hallucination）
模型生成看似合理但实际不正确或不存在的信息。

### 温度（Temperature）
控制模型输出随机性的参数，值越高输出越多样。

## E.5 开发术语

### TDD（Test-Driven Development）
测试驱动开发，先编写测试再实现功能的开发方法。

### CI/CD
持续集成/持续部署，自动化构建、测试和部署的实践。

### 重构（Refactoring）
在不改变外部行为的前提下改善代码内部结构。

### 代码审查（Code Review）
检查代码质量、发现问题的过程。

### 技术债务（Technical Debt）
为快速交付而采取的次优技术决策所累积的问题。

## E.6 安全术语

### 敏感数据（Sensitive Data）
需要保护的信息，如密码、API Key、个人身份信息等。

### 数据脱敏（Data Sanitization）
移除或替换敏感信息的过程。

### 审计日志（Audit Log）
记录系统操作和事件的日志，用于安全审计和合规。

### RBAC（Role-Based Access Control）
基于角色的访问控制，根据用户角色分配权限。

## E.7 缩写对照

| 缩写 | 全称 | 中文 |
|------|------|------|
| CLI | Command Line Interface | 命令行界面 |
| API | Application Programming Interface | 应用程序编程接口 |
| MCP | Model Context Protocol | 模型上下文协议 |
| LLM | Large Language Model | 大型语言模型 |
| TDD | Test-Driven Development | 测试驱动开发 |
| CI/CD | Continuous Integration/Continuous Deployment | 持续集成/持续部署 |
| RBAC | Role-Based Access Control | 基于角色的访问控制 |
| JWT | JSON Web Token | JSON Web 令牌 |
| SSO | Single Sign-On | 单点登录 |
| SDK | Software Development Kit | 软件开发工具包 |
