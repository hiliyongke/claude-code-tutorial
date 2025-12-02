# 第5章：基础命令全解

## 5.1 命令行参数体系

Claude Code 提供了丰富的命令行参数，用于控制其行为。本节将系统性地介绍这些参数。

### 5.1.1 参数分类概览

Claude Code 的参数可分为以下几类：

| 类别 | 用途 | 示例 |
|------|------|------|
| 会话控制 | 管理对话会话 | `--resume`, `--session` |
| 模型配置 | 选择和配置模型 | `--model`, `--max-tokens` |
| 输入输出 | 控制输入输出方式 | `-p`, `--output-format` |
| 工作环境 | 设置工作上下文 | `--cwd`, `--config` |
| 权限控制 | 管理工具权限 | `--allow`, `--deny` |
| 调试诊断 | 调试和问题排查 | `--verbose`, `--debug` |

### 5.1.2 获取帮助信息

```bash
# 查看主要帮助
claude --help

# 查看特定子命令帮助
claude config --help
claude sessions --help

# 查看版本信息
claude --version
```

## 5.2 会话控制参数

### 5.2.1 会话恢复

**--resume**

恢复之前的会话，继续上次的对话：

```bash
# 恢复最近一次会话
claude --resume

# 恢复指定会话（通过会话 ID）
claude --resume abc123def

# 恢复指定会话（通过会话名称）
claude --resume my-project-session
```

**--session**

指定会话标识符：

```bash
# 创建或继续指定名称的会话
claude --session feature-auth

# 配合其他参数使用
claude --session feature-auth --model claude-opus-4-5-20251124
```

### 5.2.2 会话列表管理

```bash
# 列出所有保存的会话
claude sessions list

# 显示详细信息
claude sessions list --verbose

# 按时间排序
claude sessions list --sort time

# 删除会话
claude sessions delete session_id

# 清理过期会话
claude sessions clean --older-than 30d
```

### 5.2.3 会话导出

```bash
# 导出为 Markdown
claude sessions export session_id --format markdown

# 导出为 JSON
claude sessions export session_id --format json

# 导出到指定文件
claude sessions export session_id -o ./exports/session.md
```

## 5.3 模型配置参数

### 5.3.1 模型选择

**--model, -m**

指定使用的 Claude 模型。支持别名或完整模型名称：

```bash
# 使用别名（推荐，简洁）
claude --model sonnet    # Claude Sonnet 4.5
claude --model opus      # Claude Opus 4.5
claude --model haiku     # Claude Haiku 4.5

# 使用完整模型名称
claude --model claude-sonnet-4-5-20250929
claude --model claude-opus-4-5-20251124
claude --model claude-haiku-4-5-20251015

# 简写形式
claude -m sonnet
```

**可用模型别名**：

| 别名 | 对应模型 | 特点 |
|------|---------|------|
| `sonnet` | claude-sonnet-4-5-20250929 | 均衡性能，推荐日常使用 |
| `opus` | claude-opus-4-5-20251124 | 最强能力，复杂任务 |
| `haiku` | claude-haiku-4-5-20251015 | 极速响应，成本最低 |

### 5.3.2 生成参数

**--max-tokens**

控制单次响应的最大 token 数：

```bash
# 设置最大 token 数
claude --max-tokens 4096

# 对于长文档生成，可以设置更大值
claude --max-tokens 16384
```

**--temperature**

控制输出的随机性（0-1）：

```bash
# 更确定性的输出（适合代码生成）
claude --temperature 0.3

# 更创造性的输出（适合头脑风暴）
claude --temperature 0.9
```

### 5.3.3 模型信息查询

```bash
# 查看可用模型列表
claude models list

# 查看模型详细信息
claude models info claude-sonnet-4-5-20250929

# 查看当前默认模型
claude models default
```

## 5.4 输入输出参数

### 5.4.1 非交互模式

**-p, --prompt**

直接传入提示词，执行单次查询：

```bash
# 简单查询
claude -p "什么是 Docker?"

# 多行提示词
claude -p "请解释以下代码的作用：
function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}"

# 从文件读取提示词
claude -p "$(cat prompt.txt)"
```

**--stdin**

从标准输入读取内容：

```bash
# 管道输入
echo "解释这段代码" | claude --stdin

# 结合文件内容
cat error.log | claude --stdin -p "分析这个错误日志"

# 处理命令输出
git diff | claude --stdin -p "审查这些代码变更"
```

### 5.4.2 输出控制

**--output-format**

指定输出格式（官方支持的选项）：

```bash
# 纯文本输出（默认）
claude -p "列出常用 Git 命令" --output-format text

# JSON 格式输出（便于脚本解析）
claude -p "列出常用 Git 命令" --output-format json

# 流式 JSON 输出（实时获取）
claude -p "列出常用 Git 命令" --output-format stream-json
```

**--json-schema**

要求输出符合指定的 JSON Schema（仅 `-p` 模式）：

```bash
# 结构化输出
claude -p "分析这个函数" --json-schema '{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "complexity": {"type": "number"},
    "suggestions": {"type": "array"}
  }
}'
```

**--include-partial-messages**

在流式输出中包含部分消息：

```bash
claude -p "生成代码" --output-format stream-json --include-partial-messages
```

**--output, -o**

将输出保存到文件：

```bash
# 保存到文件
claude -p "生成 README 模板" -o README.md

# 配合格式使用
claude -p "项目结构分析" --output-format json -o analysis.json
```

**--quiet, -q**

静默模式，减少输出信息：

```bash
# 只输出核心结果
claude -p "计算 1+1" --quiet
```

**--no-stream**

禁用流式输出，等待完整响应：

```bash
# 等待完整响应后一次性输出
claude -p "写一篇文章" --no-stream
```

### 5.4.3 输入文件

**--file, -f**

将文件内容作为上下文：

```bash
# 分析单个文件
claude -f src/index.js -p "解释这个文件的作用"

# 分析多个文件
claude -f src/auth.js -f src/user.js -p "这两个模块如何交互？"

# 配合通配符
claude -f "src/*.js" -p "分析这些文件的代码质量"
```

## 5.5 工作环境参数

### 5.5.1 工作目录

**--cwd**

指定工作目录：

```bash
# 在指定目录中工作
claude --cwd /path/to/project

# 相对路径
claude --cwd ./my-project
```

### 5.5.2 配置文件

**--config**

指定配置文件：

```bash
# 使用自定义配置
claude --config ./custom-config.json

# 使用特定环境配置
claude --config ~/.config/claude/work-config.json
```

**--no-config**

忽略配置文件，使用默认设置：

```bash
claude --no-config
```

### 5.5.3 环境变量

Claude Code 支持通过环境变量进行配置：

```bash
# API 密钥
export ANTHROPIC_API_KEY="sk-ant-..."

# 默认模型
export CLAUDE_MODEL="claude-opus-4-5-20251124"

# 配置目录
export CLAUDE_CONFIG_DIR="~/.config/claude-work"

# 代理设置
export HTTPS_PROXY="http://proxy:8080"
```

## 5.6 权限控制参数

### 5.6.1 工具权限

**--allowedTools**

允许使用的工具列表（不提示用户授权）：

```bash
# 允许 Git 相关命令
claude --allowedTools "Bash(git log:*)" "Bash(git diff:*)" "Read"

# 允许文件读取和搜索
claude --allowedTools "Read" "Grep" "Glob"
```

**--disallowedTools**

禁止使用的工具列表：

```bash
# 禁止编辑和删除
claude --disallowedTools "Edit" "Write"

# 禁止执行危险命令
claude --disallowedTools "Bash(rm:*)" "Bash(sudo:*)"
```

### 5.6.2 权限模式

**--permission-mode**

指定权限模式：

```bash
# 计划模式（只规划不执行）
claude --permission-mode plan

# 默认模式（需要确认）
claude --permission-mode default
```

**--dangerously-skip-permissions**

跳过所有权限提示（谨慎使用）：

```bash
# 仅在可信环境中使用
claude --dangerously-skip-permissions -p "执行任务"
```

### 5.6.3 路径限制

**--add-dir**

添加额外的工作目录供 Claude 访问：

```bash
# 添加多个目录
claude --add-dir ../apps ../lib

# 访问共享库
claude --add-dir ~/shared-components
```

**--denied-paths**

禁止访问的路径：

```bash
# 禁止访问敏感目录
claude --denied-paths ./secrets,./credentials

# 禁止访问配置文件
claude --denied-paths "**/.env*"
```

### 5.6.3 确认模式

**--yes, -y**

自动确认所有操作（谨慎使用）：

```bash
# 自动确认所有操作
claude -p "安装依赖并运行测试" --yes
```

**--no-confirm**

禁用特定类型的确认：

```bash
# 禁用文件操作确认
claude --no-confirm file

# 禁用命令执行确认（危险）
claude --no-confirm bash
```

## 5.7 调试诊断参数

### 5.7.1 详细输出

**--verbose, -v**

显示详细信息：

```bash
# 显示详细日志
claude --verbose

# 更详细的输出
claude -vv

# 最详细的输出
claude -vvv
```

**--debug**

启用调试模式：

```bash
# 调试模式
claude --debug

# 调试特定组件
claude --debug api
claude --debug tools
```

### 5.7.2 日志记录

**--log-file**

将日志写入文件：

```bash
# 记录日志到文件
claude --log-file ./claude.log

# 配合详细模式
claude --verbose --log-file ./debug.log
```

**--log-level**

设置日志级别：

```bash
# 只记录错误
claude --log-level error

# 记录所有信息
claude --log-level debug
```

### 5.7.3 诊断命令

```bash
# 检查系统状态
claude doctor

# 检查认证状态
claude auth status

# 检查网络连接
claude ping

# 显示配置信息
claude config show
```

## 5.8 系统提示参数

### 5.8.1 系统提示定制

**--system-prompt**

完全替换默认系统提示（交互和非交互模式均可用）：

```bash
# 自定义系统提示
claude --system-prompt "你是一名 Python 专家，专注于数据科学"

# 配合非交互模式
claude -p "分析数据" --system-prompt "你是数据分析师"
```

**--system-prompt-file**

从文件加载系统提示（仅 `-p` 模式）：

```bash
# 从文件加载
claude -p "开始工作" --system-prompt-file ./prompts/expert.txt
```

**--append-system-prompt**

在默认系统提示后追加内容（保留 Claude Code 默认能力）：

```bash
# 追加特定指令
claude --append-system-prompt "始终使用 TypeScript，遵循 ESLint 规范"

# 团队规范
claude --append-system-prompt "代码注释使用中文"
```

### 5.8.2 系统提示参数对比

| 参数 | 行为 | 适用模式 | 使用场景 |
|------|------|----------|----------|
| `--system-prompt` | 完全替换默认提示 | 交互 + 非交互 | 需要完全控制 Claude 行为 |
| `--system-prompt-file` | 从文件加载提示 | 仅非交互（`-p`） | 复用可维护的提示模板 |
| `--append-system-prompt` | 在默认提示后追加 | 交互 + 非交互 | 保留默认能力并添加特定指令 |

## 5.9 子代理参数

### 5.9.1 动态定义子代理

**--agents**

通过 JSON 动态定义自定义子代理：

```bash
# 定义代码审查员代理
claude --agents '{
  "code-reviewer": {
    "description": "专业代码审查员，在代码变更后主动使用",
    "prompt": "你是一名资深代码审查员，专注于代码质量、安全和最佳实践",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'

# 定义多个代理
claude --agents '{
  "reviewer": {
    "description": "代码审查",
    "prompt": "你是代码审查专家"
  },
  "tester": {
    "description": "测试专家",
    "prompt": "你是测试工程师，专注于编写测试用例"
  }
}'
```

### 5.9.2 子代理配置字段

| 字段 | 是否必需 | 描述 |
|------|----------|------|
| `description` | 是 | 描述子代理何时被调用 |
| `prompt` | 是 | 指导子代理行为的系统提示 |
| `tools` | 否 | 可使用的工具列表，默认继承所有 |
| `model` | 否 | 使用的模型别名（`sonnet`/`opus`/`haiku`） |

## 5.10 子命令体系

除了主命令外，Claude Code 还提供了多个子命令：

### 5.8.1 配置管理

```bash
# 查看所有配置
claude config show

# 获取特定配置
claude config get model

# 设置配置
claude config set model claude-opus-4-5-20251124

# 重置配置
claude config reset

# 编辑配置文件
claude config edit
```

### 5.8.2 认证管理

```bash
# 登录
claude auth login

# 登出
claude auth logout

# 查看认证状态
claude auth status

# 刷新认证
claude auth refresh
```

### 5.8.3 会话管理

```bash
# 列出会话
claude sessions list

# 查看会话详情
claude sessions show session_id

# 删除会话
claude sessions delete session_id

# 导出会话
claude sessions export session_id

# 清理会话
claude sessions clean
```

### 5.8.4 版本与更新

```bash
# 查看版本
claude version

# 检查更新
claude update check

# 执行更新
claude update
```

## 5.9 命令组合示例

### 5.9.1 代码审查场景

```bash
# 审查 Git 变更
git diff HEAD~1 | claude --stdin \
  -p "审查这些代码变更，指出潜在问题" \
  --model claude-opus-4-5-20251124 \
  --output-format markdown \
  -o review.md
```

### 5.9.2 批量文件处理

```bash
# 为多个文件生成文档
for file in src/*.js; do
  claude -f "$file" \
    -p "为这个文件生成 JSDoc 注释" \
    --quiet \
    -o "${file%.js}.doc.md"
done
```

### 5.9.3 CI/CD 集成

```bash
# 在 CI 中运行代码检查
claude -p "检查 src/ 目录下的代码质量问题" \
  --cwd ./project \
  --allow file \
  --deny bash \
  --output-format json \
  --no-stream \
  -o quality-report.json
```

### 5.9.4 安全受限环境

```bash
# 只读模式，禁止任何修改
claude --deny write,bash,delete \
  --allowed-paths ./src,./docs \
  -p "分析项目架构"
```

## 5.10 快捷键与交互技巧

### 5.10.1 交互模式快捷键

在交互模式下，支持以下快捷键：

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 中断当前操作 |
| `Ctrl+D` | 退出 Claude Code |
| `Ctrl+L` | 清屏 |
| `Ctrl+U` | 清除当前输入 |
| `↑` / `↓` | 浏览输入历史 |
| `Tab` | 命令/路径补全 |

### 5.10.2 输入历史

Claude Code 会记录输入历史，可以通过方向键浏览：

```bash
# 查看输入历史
> /history input

# 搜索历史
> /history search "docker"
```

### 5.10.3 命令别名

在 shell 配置中设置别名提高效率：

```bash
# ~/.bashrc 或 ~/.zshrc

# 基础别名
alias c='claude'
alias cq='claude -p'

# 常用场景别名
alias cr='claude --resume'
alias ccode='claude -p "审查这段代码"'
alias cexplain='claude -p "解释这段代码"'
alias cfix='claude -p "修复这个错误"'

# 模型快捷切换
alias copus='claude --model claude-opus-4-5-20251124'
alias chaiku='claude --model claude-3-5-haiku-20241022'
```

## 5.11 本章小结

本章全面介绍了 Claude Code 的命令行参数和子命令体系。掌握这些命令可以帮助您更高效、更灵活地使用 Claude Code，适应各种开发场景的需求。

在下一部分中，我们将深入探讨 Claude Code 的配置系统，学习如何通过配置文件定制 Claude Code 的行为。

---

**关键要点回顾**：

1. 会话控制：`--resume`、`--session` 管理对话会话
2. 模型配置：`--model`、`--max-tokens`、`--temperature` 控制模型行为
3. 输入输出：`-p`、`--stdin`、`-o` 灵活处理输入输出
4. 权限控制：`--allow`、`--deny`、`--allowed-paths` 确保安全
5. 调试诊断：`--verbose`、`--debug` 排查问题

**命令速查**：

```bash
claude -p "问题"              # 单次查询
claude --resume               # 恢复会话
claude -f file.js -p "分析"   # 分析文件
claude --model opus           # 指定模型
claude --allow file           # 允许文件操作
claude --verbose              # 详细输出
```
