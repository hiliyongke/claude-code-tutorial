# 第3章：安装与环境配置

## 3.1 系统要求

在安装 Claude Code 之前，请确保您的系统满足以下要求：

### 3.1.1 操作系统支持

| 操作系统 | 最低版本 | 推荐版本 | 备注 |
|---------|---------|---------|------|
| macOS | 10.15 (Catalina) | 14.0+ (Sonoma) | 原生支持 |
| Ubuntu/Debian | 20.04 LTS | 22.04/24.04 LTS | 原生支持 |
| Windows | Windows 10 | Windows 11 | **必须使用 WSL2** |
| 其他 Linux | - | - | 需要 glibc 2.31+ |

> **Windows 用户注意**：Claude Code 不支持原生 Windows 环境，必须通过 WSL2（Windows Subsystem for Linux 2）运行。

### 3.1.2 软件依赖

| 组件 | 最低版本 | 推荐版本 | 说明 |
|------|---------|---------|------|
| **Node.js** | v18.0.0 | v20.x LTS 或 v22.x | 必需，用于运行 Claude Code |
| npm | v8.0.0 | v10.x | 包管理器（随 Node.js 安装） |
| Git | v2.0.0 | v2.40+ | 版本控制（推荐） |

### 3.1.3 网络要求

- 稳定的互联网连接
- 能够访问 `api.anthropic.com`
- 能够访问 `registry.npmjs.org`（安装时）

### 3.1.4 账户要求

您需要以下账户之一：
- **Claude.ai 账户**（推荐）：通过 OAuth 认证
- **Anthropic Console 账户**：使用 API Key 认证

## 3.2 安装 Node.js

### 3.2.1 macOS 安装

**方式一：使用 Homebrew（推荐）**

```bash
# 安装 Homebrew（如果尚未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node.js LTS 版本
brew install node@20

# 或安装最新 LTS
brew install node

# 验证安装
node --version  # 应显示 v20.x.x 或更高
npm --version   # 应显示 v10.x.x 或更高
```

**方式二：使用 nvm（Node Version Manager）**

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# 重新加载 shell 配置
source ~/.bashrc  # 或 source ~/.zshrc

# 安装 Node.js LTS
nvm install --lts

# 设置默认版本
nvm alias default lts/*

# 验证安装
node --version
npm --version
```

### 3.2.2 Ubuntu/Debian 安装

**方式一：使用 NodeSource 仓库（推荐）**

```bash
# 安装 Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

**方式二：使用 nvm**

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# 重新加载配置
source ~/.bashrc

# 安装 Node.js LTS
nvm install --lts
nvm use --lts

# 验证
node --version
npm --version
```

### 3.2.3 Windows（WSL2）安装

**步骤1：启用 WSL2**

```powershell
# 在 PowerShell（管理员）中执行
wsl --install

# 重启计算机后，设置默认版本为 WSL2
wsl --set-default-version 2

# 安装 Ubuntu（或其他发行版）
wsl --install -d Ubuntu-22.04
```

**步骤2：在 WSL2 中安装 Node.js**

```bash
# 进入 WSL2
wsl

# 更新包列表
sudo apt update && sudo apt upgrade -y

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证
node --version
npm --version
```

## 3.3 安装 Claude Code

Claude Code 提供多种安装方式，选择最适合您环境的方式即可。

### 3.3.1 一键安装（推荐，macOS/Linux）

```bash
# 官方一键安装脚本
curl -fsSL https://claude.ai/install.sh | bash

# 验证安装
claude --version
```

### 3.3.2 使用 Homebrew 安装（macOS）

```bash
# 安装 Claude Code
brew install claude-code

# 验证安装
claude --version
```

### 3.3.3 使用 npm 全局安装

```bash
# 全局安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

如果遇到权限问题，可以使用以下方式：

```bash
# 方式一：使用 sudo（Linux/macOS）
sudo npm install -g @anthropic-ai/claude-code

# 方式二：修改 npm 全局目录权限
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @anthropic-ai/claude-code
```

### 3.3.4 验证安装

```bash
# 检查版本
claude --version

# 查看帮助
claude --help

# 检查更新
claude update
```

## 3.4 首次认证配置

### 3.4.1 启动认证流程

首次运行 Claude Code 时，会自动引导您完成认证：

```bash
# 启动 Claude Code
claude

# 或进入指定项目目录后启动
cd your-project
claude
```

### 3.4.2 认证方式选择

Claude Code 支持两种认证方式：

**方式一：OAuth 认证（推荐）**

1. 运行 `claude` 后，选择 "Login with Claude.ai"
2. 浏览器会自动打开 Anthropic 登录页面
3. 使用您的 Claude.ai 账户登录
4. 授权 Claude Code 访问
5. 返回终端，认证自动完成

**方式二：API Key 认证**

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 创建或复制 API Key
3. 设置环境变量：

```bash
# 临时设置（当前终端有效）
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# 永久设置（添加到 shell 配置文件）
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-..."' >> ~/.bashrc
source ~/.bashrc

# 或使用 Claude Code 配置
claude config set apiKey "sk-ant-api03-..."
```

### 3.4.3 首次启动配置向导

首次启动时，Claude Code 会引导您完成以下配置：

1. **选择主题**：Light / Dark / System
2. **确认安全须知**：了解工具的能力和限制
3. **终端配置**：使用默认终端设置
4. **信任工作目录**：确认当前目录为可信工作区

## 3.5 环境变量配置

### 3.5.1 核心环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `ANTHROPIC_API_KEY` | API 密钥 | `sk-ant-api03-...` |
| `ANTHROPIC_AUTH_TOKEN` | 认证令牌（二选一） | `sk-...` |
| `ANTHROPIC_BASE_URL` | API 基础 URL（可选） | `https://api.anthropic.com` |
| `CLAUDE_CODE_CONFIG_DIR` | 配置目录（可选） | `~/.claude` |

### 3.5.2 配置文件位置

Claude Code 的配置文件存储在以下位置：

| 平台 | 全局配置目录 |
|------|-------------|
| macOS | `~/.claude/` |
| Linux | `~/.claude/` |
| Windows (WSL2) | `~/.claude/` |

主要配置文件：

```
~/.claude/
├── settings.json      # 全局设置
├── credentials.json   # 认证信息（加密存储）
├── projects/          # 项目级配置缓存
└── mcp/              # MCP 服务器配置
```

### 3.5.3 全局配置文件示例

`~/.claude/settings.json`：

```json
{
  "theme": "dark",
  "preferredModel": "claude-sonnet-4-5-20250929",
  "autoCompactThreshold": 500,
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
    "ANTHROPIC_API_KEY": "your_api_key"
  },
  "permissions": {
    "allowedTools": ["Read", "Write", "Edit", "Bash"],
    "blockedCommands": ["rm -rf /", "sudo rm"]
  }
}
```

## 3.6 代理配置

### 3.6.1 HTTP 代理

如果您需要通过代理访问 Anthropic API：

```bash
# 设置 HTTP 代理
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"

# 或在配置文件中设置
claude config set proxy "http://proxy.example.com:8080"
```

### 3.6.2 国内用户配置

对于国内用户，可以使用 API 中转服务（需自行评估安全性）：

```bash
# 设置中转 API 地址
export ANTHROPIC_BASE_URL="https://your-proxy-service.com"
export ANTHROPIC_API_KEY="your-api-key"

# 或在配置文件中设置
# ~/.claude/settings.json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://your-proxy-service.com",
    "ANTHROPIC_API_KEY": "your-api-key"
  }
}
```

## 3.7 更新与卸载

### 3.7.1 更新 Claude Code

```bash
# 检查更新
claude update

# 或使用 npm 更新
npm update -g @anthropic-ai/claude-code

# 查看当前版本
claude --version
```

建议定期更新以获取最新功能和安全修复。

### 3.7.2 卸载 Claude Code

```bash
# 使用 npm 卸载
npm uninstall -g @anthropic-ai/claude-code

# 清理配置文件（可选）
rm -rf ~/.claude
```

## 3.8 常见安装问题

### 3.8.1 权限错误

**问题**：`EACCES: permission denied`

**解决方案**：

```bash
# 方案一：修改 npm 目录权限
sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}

# 方案二：使用 nvm 管理 Node.js
# nvm 安装的 Node.js 不需要 sudo
```

### 3.8.2 Node.js 版本过低

**问题**：`Node.js version must be >= 18.0.0`

**解决方案**：

```bash
# 使用 nvm 切换版本
nvm install 20
nvm use 20

# 或更新系统 Node.js
# macOS
brew upgrade node

# Ubuntu
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 3.8.3 网络连接问题

**问题**：无法连接到 npm 或 Anthropic API

**解决方案**：

```bash
# 检查网络连接
ping api.anthropic.com

# 设置 npm 镜像（如果 npm 安装慢）
npm config set registry https://registry.npmmirror.com

# 安装完成后恢复
npm config set registry https://registry.npmjs.org
```

### 3.8.4 WSL2 相关问题

**问题**：Windows 下无法运行

**解决方案**：

```powershell
# 确保 WSL2 已正确安装
wsl --status

# 如果显示 WSL1，升级到 WSL2
wsl --set-version Ubuntu-22.04 2

# 确保在 WSL2 环境中运行 Claude Code
wsl
claude
```

## 3.9 本章小结

本章详细介绍了 Claude Code 的安装和配置过程，包括：

1. 系统要求和软件依赖
2. 在不同操作系统上安装 Node.js
3. 安装 Claude Code
4. 认证配置
5. 环境变量和配置文件
6. 代理配置
7. 更新与卸载
8. 常见问题解决

完成本章的配置后，您就可以开始使用 Claude Code 进行开发工作了。下一章将介绍如何进行第一次对话，开始您的 AI 辅助编程之旅。

---

**关键要点回顾**：

1. Claude Code 需要 Node.js 18+ 环境
2. Windows 用户必须使用 WSL2
3. 推荐使用 OAuth 认证（Claude.ai 账户）
4. 配置文件存储在 `~/.claude/` 目录
5. 使用 `claude update` 保持版本更新
