# 附录 D：常见问题排查

本附录汇总了使用 Claude Code 过程中常见的问题及其解决方案。

## D.1 安装与配置问题

### 问题：安装失败

**症状**：`npm install -g @anthropic-ai/claude-cli` 失败

**解决方案**：
```bash
# 1. 检查 Node.js 版本（需要 18+）
node --version

# 2. 清除 npm 缓存
npm cache clean --force

# 3. 使用管理员权限安装
sudo npm install -g @anthropic-ai/claude-cli

# 4. 或使用 npx 直接运行
npx @anthropic-ai/claude-cli
```

### 问题：API Key 无效

**症状**：`Error: Invalid API key`

**解决方案**：
```bash
# 1. 检查环境变量
echo $ANTHROPIC_API_KEY

# 2. 重新设置 API Key
export ANTHROPIC_API_KEY="sk-ant-your-key"

# 3. 或使用配置命令
claude config set apiKey "sk-ant-your-key"

# 4. 验证 API Key 格式（应以 sk-ant- 开头）
```

### 问题：找不到 claude 命令

**症状**：`command not found: claude`

**解决方案**：
```bash
# 1. 检查全局安装路径
npm root -g

# 2. 添加到 PATH
export PATH="$PATH:$(npm root -g)/../bin"

# 3. 或重新安装
npm uninstall -g @anthropic-ai/claude-cli
npm install -g @anthropic-ai/claude-cli
```

## D.2 运行时问题

### 问题：响应超时

**症状**：请求长时间无响应或超时错误

**解决方案**：
```bash
# 1. 检查网络连接
curl -I https://api.anthropic.com

# 2. 设置更长的超时时间
claude config set timeout 120000

# 3. 使用代理（如果需要）
export HTTPS_PROXY="http://proxy:port"

# 4. 减少输入内容大小
```

### 问题：内存不足

**症状**：`JavaScript heap out of memory`

**解决方案**：
```bash
# 1. 增加 Node.js 内存限制
export NODE_OPTIONS="--max-old-space-size=4096"

# 2. 减少上下文大小
claude --max-context-tokens 50000

# 3. 清理会话历史
/clear
```

### 问题：文件读取失败

**症状**：`Error: Cannot read file`

**解决方案**：
```bash
# 1. 检查文件权限
ls -la <file>

# 2. 检查文件是否存在
test -f <file> && echo "exists"

# 3. 检查文件是否在 .claudeignore 中
cat .claudeignore

# 4. 使用绝对路径
claude "@/absolute/path/to/file"
```

## D.3 功能问题

### 问题：Hooks 不执行

**症状**：配置的 Hook 没有触发

**解决方案**：
```bash
# 1. 检查 Hook 配置
cat .claude/settings.json | jq '.hooks'

# 2. 验证 Hook 脚本权限
chmod +x .claude/hooks/*.sh

# 3. 检查 Hook 语法
node -c .claude/hooks/pre-session.js

# 4. 启用调试模式查看详情
claude --debug
```

### 问题：MCP 连接失败

**症状**：无法连接到 MCP Server

**解决方案**：
```bash
# 1. 检查 MCP Server 是否运行
ps aux | grep mcp

# 2. 验证配置
cat .claude/mcp.json

# 3. 测试连接
curl http://localhost:3000/health

# 4. 查看 MCP Server 日志
tail -f ~/.claude/logs/mcp.log
```

### 问题：Skills 加载失败

**症状**：自定义 Skill 无法使用

**解决方案**：
```bash
# 1. 检查 Skill 文件位置
ls -la .claude/skills/

# 2. 验证 YAML 语法
npx yaml-lint .claude/skills/my-skill.yaml

# 3. 检查必填字段
# name, description, instructions 都是必需的

# 4. 重新加载 Skills
/skills reload
```

## D.4 性能问题

### 问题：响应速度慢

**可能原因及解决方案**：

| 原因 | 解决方案 |
|------|---------|
| 输入过长 | 精简提示词和上下文 |
| 模型选择不当 | 简单任务使用 Haiku |
| 网络延迟 | 检查网络，使用代理 |
| 输出过长 | 设置 max_tokens 限制 |

### 问题：Token 消耗过高

**解决方案**：
```bash
# 1. 查看 Token 使用情况
/tokens

# 2. 压缩会话历史
/compact

# 3. 优化 CLAUDE.md 配置
# 移除不必要的说明

# 4. 使用更经济的模型
claude --model claude-3-haiku
```

## D.5 错误代码参考

| 错误代码 | 含义 | 解决方案 |
|---------|------|---------|
| 401 | API Key 无效 | 检查并更新 API Key |
| 403 | 权限不足 | 检查 API Key 权限 |
| 429 | 请求过于频繁 | 等待后重试，检查限流配置 |
| 500 | 服务器错误 | 稍后重试 |
| 503 | 服务不可用 | 检查 API 状态页面 |
| ECONNREFUSED | 连接被拒绝 | 检查网络和代理设置 |
| ETIMEDOUT | 连接超时 | 增加超时时间，检查网络 |

## D.6 获取帮助

如果以上方案无法解决问题：

1. **查看详细日志**：`claude --debug`
2. **检查官方文档**：https://docs.anthropic.com/claude-cli
3. **搜索 GitHub Issues**：https://github.com/anthropics/claude-cli/issues
4. **社区求助**：Discord、Stack Overflow
5. **提交 Bug 报告**：包含复现步骤、错误信息、环境信息
