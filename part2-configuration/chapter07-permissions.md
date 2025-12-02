# 第7章：权限与安全模型

## 7.1 安全设计理念

Claude Code 作为一个能够访问文件系统和执行命令的 AI 工具，其安全设计至关重要。本章将深入探讨 Claude Code 的权限控制和安全机制。

### 7.1.1 最小权限原则

Claude Code 的安全设计遵循最小权限原则（Principle of Least Privilege）：

- **默认受限**：工具默认只有最小必要权限
- **显式授权**：敏感操作需要用户明确授权
- **范围限制**：操作范围限制在工作目录内
- **可审计**：所有操作都有日志记录

### 7.1.2 安全威胁模型

Claude Code 的安全设计考虑了以下威胁场景：

| 威胁类型 | 描述 | 防护措施 |
|---------|------|---------|
| 意外文件删除 | 误删重要文件 | 操作确认、路径限制 |
| 敏感信息泄露 | 读取密钥等敏感文件 | 路径黑名单、内容过滤 |
| 恶意命令执行 | 执行危险 shell 命令 | 命令审核、白名单机制 |
| 权限提升 | 获取超出预期的权限 | 沙箱隔离、权限边界 |
| 数据外泄 | 代码发送到外部服务 | 网络控制、敏感检测 |

### 7.1.3 信任边界

理解 Claude Code 的信任边界有助于正确使用：

```mermaid
flowchart TB
    subgraph 用户终端环境
        subgraph Claude_Code进程["Claude Code 进程"]
            subgraph 安全沙箱
                文件工具
                命令工具
                网络工具
                权限控制层
            end
        end
        文件系统Shell["文件系统/Shell"]
    end
    
    文件工具 --> 权限控制层
    命令工具 --> 权限控制层
    网络工具 --> 权限控制层
    权限控制层 --> 文件系统Shell
```

## 7.2 工具权限控制

### 7.2.1 内置工具清单

Claude Code 内置了一组面向“能力”的工具，每个能力有不同的权限要求（下表中的名称是为了方便理解的示例标签，不等同于底层实现的具体 ID）：

| 工具 | 功能 | 需要权限 |
|------|------|:--------:|
| AskUserQuestion | 向用户提出选择题，获取信息或澄清问题 | 否 |
| Bash | 在环境中执行 Shell 命令 | 是 |
| BashOutput | 从后台 Bash 会话获取输出 | 否 |
| Edit | 对特定文件进行针对性编辑 | 是 |
| ExitPlanMode | 提示用户退出计划模式并开始编码 | 是 |
| Glob | 基于模式匹配查找文件 | 否 |
| Grep | 在文件内容中搜索指定模式 | 否 |
| KillShell | 根据 ID 终止正在运行的后台 Bash 会话 | 否 |
| NotebookEdit | 修改 Jupyter Notebook 单元格 | 是 |
| Read | 读取文件内容 | 否 |
| Skill | 在主对话中执行技能 | 是 |
| SlashCommand | 运行自定义斜杠命令 | 是 |
| Task | 运行子代理以处理复杂的多步骤任务 | 否 |
| TodoWrite | 创建并管理结构化任务列表 | 否 |
| WebFetch | 从指定 URL 获取内容 | 是 |
| WebSearch | 执行带有域名过滤的网页搜索 | 是 |
| List | 列出目录和文件结构等信息（目录浏览能力示例） | 否 |
| Write | 创建或覆盖文件 | 是 |

> **说明**：标记为"需要权限"的能力在使用时需要在 `settings.json` 的 `permissions` 中配置允许规则，或者需要用户确认；实际可用工具及其内部名称以当前版本 Claude Code 的内置帮助和官方文档为准。

### 7.2.2 权限配置语法

通过命令行参数控制工具权限：

```bash
# 允许特定工具
claude --allow Read,Write,Edit

# 禁止特定工具
claude --deny Bash

# 组合使用
claude --allow Read,Grep --deny Write,Edit,Bash
```

通过配置文件控制：

```json
{
  "permissions": {
    "allowedTools": ["Read", "Write", "Edit", "Grep", "Glob", "List"],
    "deniedTools": ["Bash"]
  }
}
```

通过 CLAUDE.md 控制：

```markdown
## 权限配置

### 允许的工具
- Read：读取文件
- Write：写入文件
- Edit：编辑文件
- Grep：搜索内容
- Glob：文件匹配

### 禁止的工具
- Bash：禁止执行 shell 命令
```

### 7.2.3 权限继承与覆盖

权限配置遵循以下优先级（从低到高）：

1. 系统默认权限
2. 全局配置文件权限
3. 用户配置文件权限
4. 项目 CLAUDE.md 权限
5. 命令行参数权限

高优先级配置会覆盖低优先级：

```bash
# 即使配置文件允许 Bash，命令行禁止会生效
claude --deny Bash
```

## 7.3 文件系统权限

### 7.3.1 工作目录限制

默认情况下，Claude Code 只能访问工作目录及其子目录：

```bash
# 工作目录为 /home/user/project
cd /home/user/project
claude

# Claude 可以访问：
# - /home/user/project/
# - /home/user/project/src/
# - /home/user/project/tests/

# Claude 不能访问：
# - /home/user/
# - /home/user/other-project/
# - /etc/
```

### 7.3.2 路径白名单

显式允许访问特定路径：

```bash
# 允许访问额外路径
claude --allowed-paths /home/user/shared-libs,/home/user/configs
```

配置文件方式：

```json
{
  "permissions": {
    "allowedPaths": [
      "./",
      "/home/user/shared-libs",
      "/home/user/configs"
    ]
  }
}
```

### 7.3.3 路径黑名单

禁止访问敏感路径：

```bash
# 禁止访问敏感目录
claude --denied-paths ".env*,secrets/,credentials/"
```

配置文件方式：

```json
{
  "permissions": {
    "deniedPaths": [
      ".env",
      ".env.*",
      "secrets/",
      "credentials/",
      "**/*.pem",
      "**/*.key",
      "**/id_rsa*"
    ]
  }
}
```

### 7.3.4 默认保护路径

Claude Code 默认保护以下路径模式：

```
# 敏感配置文件
.env
.env.*
*.pem
*.key
*.p12
*.pfx

# SSH 相关
.ssh/
id_rsa*
id_ed25519*

# 凭证文件
credentials*
secrets*
*.secret

# 系统目录
/etc/
/var/
/usr/
~/.config/ (除 claude 配置外)
```

### 7.3.5 文件类型限制

可以限制可操作的文件类型：

```json
{
  "permissions": {
    "allowedFileTypes": [
      ".js", ".ts", ".jsx", ".tsx",
      ".json", ".md", ".yaml", ".yml",
      ".css", ".scss", ".html"
    ],
    "deniedFileTypes": [
      ".exe", ".dll", ".so",
      ".zip", ".tar", ".gz"
    ]
  }
}
```

## 7.4 命令执行安全

### 7.4.1 命令确认机制

默认情况下，执行 shell 命令需要用户确认：

```
> 运行测试

我将执行以下命令：
$ npm test

是否允许执行此命令？
[y] 是  [n] 否  [a] 本次会话始终允许  [v] 查看命令详情
```

确认选项说明：

- **y (yes)**：允许执行此次命令
- **n (no)**：拒绝执行
- **a (always)**：本次会话中允许所有类似命令
- **v (view)**：查看命令的详细信息

### 7.4.2 命令分类与风险评估

Claude Code 对命令进行风险评估：

**低风险命令**（可能自动执行）：
```bash
ls, pwd, echo, cat, head, tail
npm test, npm run lint
git status, git log, git diff
```

**中风险命令**（需要确认）：
```bash
npm install, yarn add
git commit, git push
mkdir, touch, cp
```

**高风险命令**（强制确认 + 警告）：
```bash
rm, rm -rf
sudo, su
chmod, chown
curl | bash, wget | sh
> file (重定向覆盖)
```

### 7.4.3 命令白名单

配置允许自动执行的命令：

```json
{
  "permissions": {
    "autoApproveCommands": [
      "npm test",
      "npm run lint",
      "npm run build",
      "git status",
      "git diff"
    ]
  }
}
```

CLAUDE.md 方式：

```markdown
## 命令权限

### 自动批准的命令
以下命令可以无需确认直接执行：
- `npm test`
- `npm run lint`
- `npm run typecheck`
- `git status`
- `git diff`
```

### 7.4.4 命令黑名单

禁止执行的命令模式：

```json
{
  "permissions": {
    "blockedCommands": [
      "rm -rf /",
      "rm -rf ~",
      "sudo *",
      "chmod 777 *",
      "curl * | bash",
      "> /dev/*"
    ]
  }
}
```

### 7.4.5 命令沙箱

对于需要更强隔离的场景，可以启用命令沙箱：

```bash
# 在 Docker 容器中执行命令
claude --sandbox docker

# 使用 firejail 沙箱
claude --sandbox firejail
```

配置文件：

```json
{
  "sandbox": {
    "enabled": true,
    "type": "docker",
    "image": "node:20-alpine",
    "mountWorkdir": true,
    "networkAccess": false
  }
}
```

## 7.5 敏感信息保护

### 7.5.1 敏感信息检测

Claude Code 会自动检测并保护敏感信息：

**检测的敏感模式**：
- API 密钥：`sk-`, `api_key`, `apikey`
- 密码：`password`, `passwd`, `secret`
- Token：`token`, `bearer`, `jwt`
- 私钥：`-----BEGIN.*PRIVATE KEY-----`
- 数据库连接：`mysql://`, `postgres://`, `mongodb://`

### 7.5.2 敏感信息处理策略

当检测到敏感信息时的处理方式：

```json
{
  "security": {
    "sensitiveDataHandling": {
      "mode": "mask",  // mask, warn, block
      "patterns": [
        "password\\s*=\\s*['\"].*['\"]",
        "api[_-]?key\\s*=\\s*['\"].*['\"]"
      ]
    }
  }
}
```

处理模式说明：

- **mask**：用 `***` 替换敏感内容后继续
- **warn**：显示警告但继续处理
- **block**：阻止操作并提示用户

### 7.5.3 环境变量安全

处理环境变量的安全策略：

```markdown
## 安全配置

### 环境变量处理
- 不要在代码中硬编码环境变量的值
- 读取 .env 文件时，只显示变量名，不显示值
- 生成配置示例时，使用占位符而非真实值

### 示例
正确：`DATABASE_URL=<your-database-url>`
错误：`DATABASE_URL=postgres://user:pass@host/db`
```

### 7.5.4 日志脱敏

Claude Code 的日志会自动脱敏：

```
# 原始内容
Connecting to postgres://admin:secret123@db.example.com/mydb

# 日志记录
Connecting to postgres://***:***@db.example.com/mydb
```

配置日志脱敏规则：

```json
{
  "logging": {
    "sanitize": true,
    "sanitizePatterns": [
      "(password[=:]\\s*)[^\\s]+",
      "(api[_-]?key[=:]\\s*)[^\\s]+",
      "([a-zA-Z]+://[^:]+:)[^@]+(@)"
    ]
  }
}
```

## 7.6 网络安全

### 7.6.1 API 通信安全

Claude Code 与 Anthropic API 的通信安全措施：

- **TLS 加密**：所有通信使用 TLS 1.3
- **证书验证**：验证服务器证书有效性
- **API 密钥保护**：密钥仅在内存中，不写入日志

### 7.6.2 代理配置安全

使用代理时的安全考虑：

```bash
# 使用 HTTPS 代理
export HTTPS_PROXY=https://proxy.company.com:8080

# 配置代理认证（注意保护凭证）
export HTTPS_PROXY=https://user:pass@proxy.company.com:8080
```

建议使用环境变量或凭证管理器存储代理凭证，避免在配置文件中明文存储。

### 7.6.3 数据传输考量

理解数据传输的范围：

**会发送到 Anthropic 服务器的数据**：
- 用户输入的提示词
- Claude 读取的文件内容（用于分析）
- 命令执行的输出（用于理解结果）

**不会发送的数据**：
- 被路径黑名单保护的文件
- 被敏感信息检测拦截的内容
- 本地配置和凭证

### 7.6.4 离线模式

对于高度敏感的环境，可以考虑：

```json
{
  "network": {
    "offlineMode": false,
    "allowedHosts": [
      "api.anthropic.com"
    ],
    "blockExternalRequests": true
  }
}
```

## 7.7 审计与日志

### 7.7.1 操作日志

Claude Code 记录所有重要操作：

```
# 日志位置
~/.config/claude/logs/

# 日志格式
[2024-12-01T10:30:45.123Z] [INFO] Session started: abc123
[2024-12-01T10:30:46.456Z] [INFO] Tool: Read file: src/index.js
[2024-12-01T10:30:47.789Z] [WARN] Sensitive pattern detected, masked
[2024-12-01T10:30:48.012Z] [INFO] Tool: Execute command: npm test (approved)
```

### 7.7.2 审计日志配置

```json
{
  "audit": {
    "enabled": true,
    "logPath": "~/.config/claude/audit/",
    "retention": "90d",
    "includeContent": false,
    "events": [
      "session.start",
      "session.end",
      "tool.execute",
      "permission.denied",
      "sensitive.detected"
    ]
  }
}
```

### 7.7.3 企业审计集成

对于企业环境，支持将审计日志发送到外部系统：

```json
{
  "audit": {
    "enabled": true,
    "exporters": [
      {
        "type": "syslog",
        "host": "syslog.company.com",
        "port": 514
      },
      {
        "type": "webhook",
        "url": "https://audit.company.com/api/events",
        "headers": {
          "Authorization": "Bearer ${AUDIT_TOKEN}"
        }
      }
    ]
  }
}
```

## 7.8 安全最佳实践

### 7.8.1 日常使用建议

1. **保持确认机制开启**：不要轻易使用 `--yes` 参数
2. **定期审查权限**：检查配置的权限是否仍然必要
3. **使用路径限制**：明确限制可访问的目录范围
4. **保护敏感文件**：确保 .env 等文件在黑名单中

### 7.8.2 团队使用建议

1. **统一安全配置**：通过项目 CLAUDE.md 统一团队的安全配置
2. **代码审查**：将 Claude 的修改纳入正常的代码审查流程
3. **权限分级**：根据项目敏感度设置不同的权限级别
4. **定期培训**：确保团队成员了解安全风险和最佳实践

### 7.8.3 敏感项目建议

对于高度敏感的项目：

```markdown
## 安全配置（敏感项目）

### 工具限制
- 禁用 Bash 工具
- 禁用 Write 工具（只允许 Edit）
- 所有操作需要确认

### 路径限制
- 只允许访问 src/ 目录
- 禁止访问所有配置文件
- 禁止访问测试数据目录

### 内容限制
- 启用严格的敏感信息检测
- 禁止读取包含 "confidential" 标记的文件
```

## 7.9 本章小结

本章详细介绍了 Claude Code 的权限与安全模型，包括工具权限控制、文件系统权限、命令执行安全、敏感信息保护和审计日志。正确配置这些安全机制是安全使用 Claude Code 的基础。

在下一章中，我们将探讨多环境配置管理，学习如何在不同环境中使用不同的配置。

---

**关键要点回顾**：

1. Claude Code 遵循最小权限原则，默认受限
2. 工具权限可通过命令行、配置文件、CLAUDE.md 控制
3. 文件系统权限通过路径白名单/黑名单控制
4. 命令执行有风险评估和确认机制
5. 敏感信息会被自动检测和保护
6. 所有操作都有审计日志记录

**安全检查清单**：

- [ ] 确认敏感路径在黑名单中
- [ ] 确认不需要的工具已禁用
- [ ] 确认命令确认机制已开启
- [ ] 确认审计日志已配置
- [ ] 确认团队成员了解安全规范
