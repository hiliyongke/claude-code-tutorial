# Claude Code 完全指南：从入门到精通

> 一本系统、深入、实用的 Claude Code 智能编程工具教程
> 
> 内容以 Claude 3.5 / 4.5 及之后的最新模型能力为参考编写

## 关于本书

本书是一本全面介绍 **Claude Code**（Anthropic 官方智能编程工具）的技术教程，旨在帮助开发者从零开始掌握这一强大的 AI 编程助手工具。无论您是初次接触 AI 辅助编程的新手，还是希望深入挖掘 Claude Code 高级功能的资深开发者，本书都将为您提供系统性的知识体系和实践指导。

### 什么是 Claude Code？

Claude Code 是 Anthropic 公司推出的 **Agentic Coding Tool**（智能编程工具），通过 npm 包 `@anthropic-ai/claude-code` 分发。它能够：

- 在终端中直接运行，理解完整代码库
- 自主规划任务、执行命令、修改文件
- 支持长达 7 小时的连续自主工作（Claude Opus 4.5）
- 通过 MCP 协议连接外部数据源和服务
- 与 GitHub Actions 深度集成

### 2025年重要更新（示例时间线）

| 时间 | 更新内容 |
|------|---------|
| 2025年5月 | Claude 4 系列发布（Opus 4、Sonnet 4） |
| 2025年7月 | 远程 MCP 服务器支持 |
| 2025年9月 | Claude Sonnet 4.5 与 Claude Agent SDK 推出 |
| 2025年10月 | Claude Haiku 4.5 发布 |
| 2025年11月 | Claude Opus 4.5 上线，面向复杂编码场景的旗舰模型 |

## 本书特色

- **系统性**：从基础概念到高级应用，循序渐进，构建完整知识体系
- **实用性**：大量真实案例和最佳实践，学以致用
- **深度性**：深入技术原理，知其然更知其所以然
- **前沿性**：涵盖 2025 年最新功能特性，紧跟技术发展

## 目录结构

### 第一部分：入门篇（了解与起步）

- [第1章：初识 Claude Code](part1-introduction/chapter01-introduction.md)
- [第2章：发展历程与技术演进](part1-introduction/chapter02-history.md)
- [第3章：安装与环境配置](part1-introduction/chapter03-installation.md)
- [第4章：第一次对话](part1-introduction/chapter04-first-conversation.md)
- [第5章：基础命令全解](part1-introduction/chapter05-basic-commands.md)

### 第二部分：配置篇（个性化定制）

- [第6章：CLAUDE.md 配置详解](part2-configuration/chapter06-claude-md.md)
- [第7章：权限与安全模型](part2-configuration/chapter07-permissions.md)
- [第8章：多环境配置管理](part2-configuration/chapter08-multi-environment.md)

### 第三部分：进阶篇（深入理解）

- [第9章：会话与上下文管理](part3-intermediate/chapter09-session-context.md)
- [第10章：文件与代码操作](part3-intermediate/chapter10-file-operations.md)
- [第11章：技术架构深度解析](part3-intermediate/chapter11-architecture.md)
- [第12章：提示词工程](part3-intermediate/chapter12-prompt-engineering.md)
- [第13章：Headless 模式与脚本集成](part3-intermediate/chapter13-headless-mode.md)

### 第四部分：高级篇（能力扩展）

- [第14章：Hooks 自动化机制](part4-advanced/chapter14-hooks.md)
- [第15章：Skills 能力扩展系统](part4-advanced/chapter15-skills.md)
- [第16章：Spec 规范驱动开发](part4-advanced/chapter16-spec.md)
- [第17章：MCP 协议与生态](part4-advanced/chapter17-mcp.md)

### 第五部分：工作流篇（效率提升）

- [第18章：常见工作流模式](part5-workflow/chapter18-workflow-patterns.md)
- [第19章：与开发工具集成](part5-workflow/chapter19-tool-integration.md)
- [第20章：多语言开发指南](part5-workflow/chapter20-multilang.md)

### 第六部分：实战篇（项目实践）

- [第21章：从零构建全栈项目](part6-practice/chapter21-fullstack-project.md)
- [第22章：遗留代码重构实战](part6-practice/chapter22-refactoring.md)
- [第23章：自动化测试体系搭建](part6-practice/chapter23-testing.md)
- [第24章：CI/CD 流水线集成](part6-practice/chapter24-cicd.md)

### 第七部分：精通篇（企业与未来）

- [第25章：企业级部署方案](part7-mastery/chapter25-enterprise.md)
- [第26章：成本控制与优化](part7-mastery/chapter26-cost.md)
- [第27章：性能调优指南](part7-mastery/chapter27-performance.md)
- [第28章：安全最佳实践](part7-mastery/chapter28-security.md)
- [第29章：未来展望与持续学习](part7-mastery/chapter29-future.md)

### 附录

- [附录A：命令速查表](appendix/appendix-a-cheatsheet.md)
- [附录B：功能决策树](appendix/appendix-b-decision-tree.md)
- [附录C：版本对比表](appendix/appendix-c-version-comparison.md)
- [附录D：常见问题排查](appendix/appendix-d-troubleshooting.md)
- [附录E：术语表](appendix/appendix-e-glossary.md)
- [附录F：学习资源汇总](appendix/appendix-f-resources.md)
- [附录G：新名词与新技术术语表](appendix/appendix-g-glossary-new-terms.md)

## 快速开始

```bash
# 推荐：使用官方安装脚本
curl -fsSL https://claude.ai/install.sh | bash

# 进入你的项目目录
cd your-project

# 启动 Claude Code
claude
```

如果你所在的环境更适合通过 npm 安装，也可以使用：

```bash
# 可选：通过 npm 全局安装
npm install -g @anthropic-ai/claude-code

claude --version
claude
```

## 适用读者

- 希望提升编程效率的软件开发者
- 对 AI 辅助编程感兴趣的技术人员
- 需要在团队中推广 AI 工具的技术负责人
- 希望深入了解 Claude Code 技术原理的研究者

## 阅读建议

1. **初学者**：建议从第一部分开始，按顺序阅读，打好基础
2. **有经验的用户**：可直接跳至感兴趣的章节，按需阅读
3. **技术负责人**：重点关注第七部分的企业级内容
4. **想了解新概念**：参阅附录G《新名词与新技术术语表》

## 版本说明

- **本书版本**：以 Claude 3.5 / 4.5 及之后的最新模型系列为参考
- **Claude Code 版本**：以官方最新稳定版本为基准编写，具体以文档为准
- **Claude 模型**：示例主要基于 Claude 3.5、Sonnet 4.x、Opus 4.x 等模型能力
- **MCP 协议**：示例包含 2025 年前后引入的远程服务器与工具集成功能

部分功能可能随版本更新而变化，建议读者结合[官方文档](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)获取最新信息。

## 相关资源

| 资源 | 链接 |
|------|------|
| Anthropic 官网 | https://www.anthropic.com |
| Claude Code 文档 | https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview |
| MCP 协议规范 | https://spec.modelcontextprotocol.io |
| npm 包 | https://www.npmjs.com/package/@anthropic-ai/claude-code |

## 反馈与贡献

如发现内容错误或有改进建议，欢迎提出反馈。

---

