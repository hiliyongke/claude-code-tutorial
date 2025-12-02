# 第4章：第一次对话

## 4.1 启动 Claude Code

完成安装和配置后，让我们开始第一次与 Claude 的对话。

### 4.1.1 基本启动方式

在终端中输入以下命令启动 Claude Code：

```bash
claude
```

如果这是首次运行且尚未配置认证，系统会引导您完成认证流程。认证成功后，您将看到类似以下的欢迎界面：

```
╭──────────────────────────────────────────────────────────────────╮
│                                                                  │
│   Claude Code v1.x.x                                             │
│   Type your message and press Enter to chat with Claude.        │
│   Type /help for available commands.                            │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯

>
```

### 4.1.2 指定工作目录

Claude Code 默认在当前目录工作。如果需要在特定项目目录中工作：

```bash
# 方式一：先切换目录
cd /path/to/your/project
claude

# 方式二：使用参数指定
claude --cwd /path/to/your/project
```

工作目录决定了 Claude 可以访问的文件范围，这对于项目相关的任务非常重要。

### 4.1.3 启动参数概览

Claude Code 支持多种启动参数：

```bash
# 指定模型
# 指定模型（支持别名或完整名称）
claude --model opus                    # 使用别名
claude --model claude-opus-4-5-20251124  # 使用完整名称

# 恢复上次会话
claude --resume

# 恢复特定会话
claude --resume session_id

# 以非交互模式执行单次查询
claude -p "你的问题"

# 组合使用
claude --model sonnet --cwd ./my-project
```

## 4.2 基础对话交互

### 4.2.1 发送消息

在提示符 `>` 后输入您的消息，按 Enter 发送：

```
> 你好，请介绍一下你自己

我是 Claude，由 Anthropic 开发的 AI 助手。在这个命令行环境中，我可以帮助您：

1. 回答编程相关问题
2. 阅读和分析代码文件
3. 生成和修改代码
4. 执行 shell 命令（需要您的确认）
5. 搜索项目中的代码

请告诉我您需要什么帮助？
```

### 4.2.2 多行输入

对于需要多行输入的场景（如粘贴代码块），有以下方式：

**方式一：使用反斜杠续行**

```
> 请解释这段代码：\
  function add(a, b) {\
    return a + b;\
  }
```

**方式二：使用引号包裹**

```
> 请解释这段代码：
"""
function add(a, b) {
  return a + b;
}
"""
```

**方式三：使用编辑器模式**

输入 `/editor` 命令打开外部编辑器编写长文本。

### 4.2.3 对话上下文

Claude Code 会自动维护对话上下文，您可以进行连续的对话：

```
> 什么是 React Hooks？

React Hooks 是 React 16.8 引入的特性，允许在函数组件中使用状态和其他 React 特性...

> 给我一个 useState 的例子

基于我们刚才讨论的 React Hooks，这里是一个 useState 的示例：

import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      点击次数：{count}
    </button>
  );
}

> 如何在这个基础上添加 useEffect？

在刚才的 Counter 组件基础上，我们可以添加 useEffect 来处理副作用...
```

注意 Claude 如何记住之前的对话内容，并在此基础上继续。

## 4.3 内置命令

Claude Code 提供了一系列以 `/` 开头的内置命令，用于控制会话和系统行为。

### 4.3.1 帮助命令

```
> /help

可用命令：
  /help           显示帮助信息
  /clear          清除当前会话历史
  /history        显示会话历史
  /save           保存当前会话
  /load           加载已保存的会话
  /model          切换或查看当前模型
  /config         查看或修改配置
  /exit           退出 Claude Code
  ...
```

### 4.3.2 会话管理命令

**清除会话**

```
> /clear

会话历史已清除。开始新的对话。
```

**查看历史**

```
> /history

会话历史（最近 10 条）：
1. [用户] 你好，请介绍一下你自己
2. [Claude] 我是 Claude，由 Anthropic 开发的 AI 助手...
3. [用户] 什么是 React Hooks？
...
```

**保存会话**

```
> /save my-react-session

会话已保存为：my-react-session
路径：~/.config/claude/sessions/my-react-session.json
```

**加载会话**

```
> /load my-react-session

已加载会话：my-react-session
包含 15 条消息，上次更新：2024-12-01 14:30
```

### 4.3.3 模型相关命令

**查看当前模型**

```
> /model

当前模型：claude-sonnet-4-5-20250929
可用模型：
  - claude-sonnet-4-5-20250929 (默认)
  - claude-opus-4-5-20251124
  - claude-3-5-haiku-20241022
```

**切换模型**

```
> /model claude-opus-4-5-20251124

已切换到模型：claude-opus-4-5-20251124
```

### 4.3.4 配置命令

```
> /config

当前配置：
  model: claude-sonnet-4-5-20250929
  maxTokens: 8192
  temperature: 0.7
  autoSave: true
  confirmBeforeExecute: true

使用 /config set <key> <value> 修改配置
```

### 4.3.5 退出命令

```
> /exit

确认退出？当前会话将自动保存。(y/n) y

会话已保存。再见！
```

也可以使用 `Ctrl+D` 或 `Ctrl+C` 退出。

## 4.4 文件操作初体验

Claude Code 最强大的能力之一是直接操作项目文件。让我们通过简单的例子体验这一功能。

### 4.4.1 读取文件

```
> 读取 package.json 文件的内容

我来读取 package.json 文件：

[读取文件: package.json]

文件内容如下：
{
  "name": "my-project",
  "version": "1.0.0",
  "description": "A sample project",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}

这是一个 Node.js 项目，使用 Express 框架，包含启动和测试脚本。
```

### 4.4.2 分析项目结构

```
> 分析这个项目的目录结构

我来查看项目结构：

[列出目录: .]

项目结构如下：
.
├── src/
│   ├── index.js
│   ├── routes/
│   │   └── api.js
│   └── utils/
│       └── helpers.js
├── tests/
│   └── api.test.js
├── package.json
└── README.md

这是一个典型的 Express 项目结构：
- src/：源代码目录
- src/routes/：API 路由定义
- src/utils/：工具函数
- tests/：测试文件
```

### 4.4.3 创建文件

```
> 在 src/utils/ 下创建一个简单的日志工具 logger.js

我将创建日志工具文件：

[创建文件: src/utils/logger.js]

已创建 src/utils/logger.js，内容如下：

const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
};

let currentLevel = LOG_LEVELS.INFO;

const logger = {
  setLevel(level) {
    currentLevel = LOG_LEVELS[level] || LOG_LEVELS.INFO;
  },
  
  debug(...args) {
    if (currentLevel <= LOG_LEVELS.DEBUG) {
      console.log('[DEBUG]', new Date().toISOString(), ...args);
    }
  },
  
  info(...args) {
    if (currentLevel <= LOG_LEVELS.INFO) {
      console.log('[INFO]', new Date().toISOString(), ...args);
    }
  },
  
  warn(...args) {
    if (currentLevel <= LOG_LEVELS.WARN) {
      console.warn('[WARN]', new Date().toISOString(), ...args);
    }
  },
  
  error(...args) {
    if (currentLevel <= LOG_LEVELS.ERROR) {
      console.error('[ERROR]', new Date().toISOString(), ...args);
    }
  }
};

module.exports = logger;

文件已创建。您可以通过 require('./utils/logger') 使用它。
```

### 4.4.4 修改文件

```
> 在 logger.js 中添加一个 fatal 级别

我将修改 logger.js 文件：

[修改文件: src/utils/logger.js]

已添加 FATAL 级别。修改内容：

1. 在 LOG_LEVELS 中添加：
   FATAL: 4

2. 添加 fatal 方法：
   fatal(...args) {
     console.error('[FATAL]', new Date().toISOString(), ...args);
     process.exit(1);
   }

修改已完成。
```

## 4.5 命令执行初体验

Claude Code 可以在您的授权下执行 shell 命令。

### 4.5.1 执行简单命令

```
> 运行 npm test 查看测试结果

我将执行测试命令：

[执行命令: npm test]
是否允许执行此命令？(y/n) y

执行结果：
 PASS  tests/api.test.js
  API Tests
    ✓ GET /api/health returns 200 (15ms)
    ✓ GET /api/users returns user list (23ms)
    ✓ POST /api/users creates new user (18ms)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total

所有测试通过。
```

### 4.5.2 命令确认机制

默认情况下，Claude Code 在执行命令前会请求确认。这是一个重要的安全机制：

```
> 删除 node_modules 目录

我将执行删除命令：

[执行命令: rm -rf node_modules]
⚠️ 警告：这是一个破坏性操作
是否允许执行此命令？(y/n) 
```

您可以：
- 输入 `y` 确认执行
- 输入 `n` 拒绝执行
- 输入 `a` 在本次会话中始终允许此类命令

### 4.5.3 查看命令输出

对于输出较长的命令，Claude 会智能截取关键信息：

```
> 运行 npm install 并告诉我安装了哪些包

[执行命令: npm install]
是否允许执行此命令？(y/n) y

命令执行完成。安装摘要：
- 新增 45 个包
- 主要依赖：
  - express@4.18.2
  - lodash@4.17.21
  - axios@1.6.0
- 开发依赖：
  - jest@29.7.0
  - eslint@8.54.0

总计安装大小：12.3 MB
```

## 4.6 实用对话技巧

### 4.6.1 明确的指令

提供清晰、具体的指令可以获得更好的结果：

```
# 不够明确
> 优化这个代码

# 更明确
> 优化 src/utils/helpers.js 中的 processData 函数，
  重点关注性能和可读性，保持接口不变
```

### 4.6.2 提供上下文

当处理复杂任务时，提供必要的背景信息：

```
> 这是一个 React 18 项目，使用 TypeScript 和 Zustand 状态管理。
  请帮我在 src/stores/ 下创建一个用户状态管理 store。
```

### 4.6.3 分步骤处理

对于复杂任务，可以分步骤进行：

```
> 我想重构用户认证模块，请先分析当前的实现

[Claude 分析现有代码]

> 好的，请给出重构方案，但先不要修改代码

[Claude 提供重构方案]

> 方案看起来不错，请开始实施第一步：提取公共接口
```

### 4.6.4 请求解释

当 Claude 执行操作后，可以请求解释：

```
> 解释一下你刚才对 auth.js 做的修改

我对 auth.js 做了以下修改：

1. 提取了 validateToken 函数（第 15-28 行）
   - 原因：这段逻辑在多处重复使用
   - 效果：提高代码复用性，便于单独测试

2. 添加了错误处理（第 32-40 行）
   - 原因：原代码没有处理网络错误
   - 效果：提高系统健壮性

3. 优化了 token 刷新逻辑（第 45-60 行）
   - 原因：原实现存在竞态条件
   - 效果：避免并发请求时的重复刷新
```

## 4.7 会话管理

### 4.7.1 会话的自动保存

Claude Code 默认会自动保存会话，您可以随时恢复：

```bash
# 列出已保存的会话
claude sessions list

# 恢复最近的会话
claude --resume

# 恢复特定会话
claude --resume session_20241201_143022
```

### 4.7.2 会话命名

为重要的会话命名，便于后续查找：

```
> /save refactor-auth-module

会话已保存为：refactor-auth-module
```

### 4.7.3 会话导出

可以将会话导出为可读格式：

```
> /export markdown

会话已导出至：./claude-session-20241201.md
```

## 4.8 本章小结

本章通过实际操作，带您完成了与 Claude Code 的第一次对话。我们学习了基本的对话交互、内置命令、文件操作和命令执行。这些是使用 Claude Code 的基础技能。

在下一章中，我们将全面介绍 Claude Code 的各种命令和参数，帮助您更高效地使用这一工具。

---

**关键要点回顾**：

1. 使用 `claude` 命令启动交互式会话
2. 内置命令以 `/` 开头，如 `/help`、`/clear`、`/save`
3. Claude 可以读取、创建、修改项目文件
4. 命令执行前会请求用户确认，确保安全
5. 会话会自动保存，可随时恢复

**练习建议**：

1. 在一个测试项目中启动 Claude Code
2. 尝试让 Claude 分析项目结构
3. 创建一个简单的工具函数
4. 运行项目的测试命令
5. 保存并恢复会话
