# 附录 A：命令速查表

本附录提供 Claude Code 常用命令的快速参考。

## A.1 基础命令

### 启动与退出

| 命令 | 说明 |
|------|------|
| `claude` | 启动交互式 REPL |
| `claude "查询"` | 带初始提示启动 REPL |
| `claude -p "查询"` | 非交互模式（SDK 模式） |
| `claude -c` | 继续最近的对话 |
| `claude update` | 更新版本 |
| `claude --help` | 显示帮助信息 |
| `claude --version` | 显示版本信息 |
| `/exit` | 退出会话 |
| `Ctrl+C` | 中断当前操作 |

### 会话管理

| 命令 | 说明 |
|------|------|
| `claude --resume` | 恢复上次会话 |
| `claude -r "<会话ID>"` | 恢复指定会话 |
| `/clear` | 清除当前会话上下文 |
| `/compact` | 压缩会话历史 |
| `/sessions` | 列出所有会话 |

## A.2 模型与配置

### 模型选择（支持别名）

| 命令 | 说明 |
|------|------|
| `claude --model sonnet` | 使用 Claude Sonnet 4.5（推荐） |
| `claude --model opus` | 使用 Claude Opus 4.5（最强） |
| `claude --model haiku` | 使用 Claude Haiku 4.5（最快） |
| `/model <name>` | 切换模型 |

### 配置管理

| 命令 | 说明 |
|------|------|
| `claude config list` | 列出所有配置 |
| `claude config get <key>` | 获取配置值 |
| `claude config set <key> <value>` | 设置配置值 |
| `claude config reset` | 重置配置 |

### Memory 管理

| 命令 | 说明 |
|------|------|
| `# 记忆内容` | 快速添加记忆 |
| `/memory` | 编辑记忆文件 |
| `/init` | 初始化项目配置 |

## A.3 文件操作

### 读取文件

| 命令 | 说明 |
|------|------|
| `@file.txt` | 引用文件内容 |
| `@src/` | 引用目录 |
| `@*.js` | 引用匹配的文件 |

### 输出控制

| 命令 | 说明 |
|------|------|
| `--output file.txt` | 输出到文件 |
| `--output-format json` | JSON 格式输出 |
| `--output-format stream-json` | 流式 JSON 输出 |
| `--json-schema '{...}'` | 结构化输出 |

## A.4 工具与权限控制

### 权限管理

| 命令 | 说明 |
|------|------|
| `--allowedTools "Read" "Write"` | 允许指定工具 |
| `--disallowedTools "Bash"` | 禁用指定工具 |
| `--permission-mode plan` | 计划模式 |
| `--dangerously-skip-permissions` | 跳过权限确认（慎用） |

### 常用工具

| 工具 | 说明 |
|------|------|
| `Read` | 读取文件 |
| `Write` | 写入文件 |
| `Edit` | 编辑文件 |
| `Bash` | 执行命令 |
| `Glob` | 文件匹配 |
| `Grep` | 内容搜索 |
| `LS` | 目录列表 |

## A.5 系统提示

| 命令 | 说明 |
|------|------|
| `--system-prompt "..."` | 完全替换系统提示 |
| `--system-prompt-file ./prompt.txt` | 从文件加载提示 |
| `--append-system-prompt "..."` | 追加系统提示 |

## A.6 子代理

| 命令 | 说明 |
|------|------|
| `--agents '{...}'` | 定义自定义子代理 |
| `--max-turns 3` | 限制代理轮次 |

## A.7 高级功能

### Hooks

| 命令 | 说明 |
|------|------|
| `/hooks` | 列出所有 Hooks |
| `/hooks enable <name>` | 启用 Hook |
| `/hooks disable <name>` | 禁用 Hook |

### Skills

| 命令 | 说明 |
|------|------|
| `/skills` | 列出所有 Skills |
| `/skill <name>` | 使用指定 Skill |

### MCP

| 命令 | 说明 |
|------|------|
| `/mcp` | 列出 MCP 服务器 |
| `/mcp connect <server>` | 连接 MCP 服务器 |
| `/mcp disconnect <server>` | 断开连接 |

## A.6 调试与诊断

| 命令 | 说明 |
|------|------|
| `claude --verbose` | 详细输出模式 |
| `claude --debug` | 调试模式 |
| `/status` | 显示当前状态 |
| `/tokens` | 显示 Token 使用情况 |

## A.7 快捷键

| 快捷键 | 说明 |
|--------|------|
| `Ctrl+C` | 中断当前操作 |
| `Ctrl+D` | 退出会话 |
| `↑` / `↓` | 浏览历史命令 |
| `Tab` | 自动补全 |
| `Ctrl+L` | 清屏 |
