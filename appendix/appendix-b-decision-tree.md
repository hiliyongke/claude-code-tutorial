# 附录 B：功能决策树

本附录提供使用 Claude Code 时的功能选择指南，帮助您在不同场景下选择合适的功能和配置。

## B.1 模型选择决策树

```mermaid
flowchart TD
    A[开始] --> B{任务是否涉及复杂推理?}
    B -->|是| C[使用 Claude Opus]
    B -->|否| D{任务是否需要高质量输出?}
    D -->|是| E[使用 Claude Sonnet]
    D -->|否| F{任务是否简单/重复?}
    F -->|是| G[使用 Claude Haiku]
    F -->|否| H[使用 Claude Sonnet - 默认]
```

## B.2 功能选择决策树

```mermaid
flowchart TD
    A[需求类型] --> B[自动化任务]
    A --> C[扩展能力]
    A --> D[项目配置]
    A --> E[规范驱动开发]
    
    B --> B1[使用 Hooks]
    B1 --> B2[会话开始 → PreSession Hook]
    B1 --> B3[会话结束 → PostSession Hook]
    B1 --> B4[工具调用前 → PreToolUse Hook]
    B1 --> B5[工具调用后 → PostToolUse Hook]
    
    C --> C1[使用 Skills 或 MCP]
    C1 --> C2[自定义提示词模板 → Skills]
    C1 --> C3[集成外部服务 → MCP Server]
    C1 --> C4[访问外部数据 → MCP Server]
    
    D --> D1[使用 CLAUDE.md]
    D1 --> D2[项目级 → 项目根目录]
    D1 --> D3[用户级 → ~/.claude/]
    
    E --> E1[使用 Spec]
    E1 --> E2[新功能开发 → 创建 Spec 文档]
    E1 --> E3[复杂任务分解 → Spec 任务列表]
```

## B.3 工作流选择指南

| 场景 | 推荐工作流 | 关键配置 |
|------|-----------|---------|
| 新功能开发 | Spec 驱动 | 创建 spec.md |
| Bug 修复 | 直接对话 | 提供错误信息 |
| 代码审查 | 批量处理 | 使用 @目录 引用 |
| 重构 | 分步执行 | 使用 Hooks 验证 |
| 文档生成 | 模板驱动 | 使用 Skills |
| 测试编写 | TDD 工作流 | 先生成测试 |

## B.4 权限配置决策

```
安全需求级别
  │
  ├─ 高（生产环境）
  │     │
  │     ├─ 禁用 Bash 工具
  │     ├─ 限制文件访问路径
  │     └─ 启用审计日志
  │
  ├─ 中（开发环境）
  │     │
  │     ├─ 允许常用工具
  │     ├─ 排除敏感目录
  │     └─ 保持默认权限
  │
  └─ 低（个人实验）
        │
        └─ 可使用 --dangerously-skip-permissions
```

## B.5 成本优化决策

```
成本敏感度
  │
  ├─ 高
  │     │
  │     ├─ 优先使用 Haiku
  │     ├─ 启用响应缓存
  │     ├─ 精简上下文
  │     └─ 批量处理请求
  │
  ├─ 中
  │     │
  │     ├─ 默认使用 Sonnet
  │     ├─ 复杂任务用 Opus
  │     └─ 监控使用量
  │
  └─ 低
        │
        └─ 根据任务需要选择模型
```
