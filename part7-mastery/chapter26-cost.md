# 第26章：成本控制与优化

Claude Code 的使用涉及 API 调用成本，对于个人开发者和企业团队而言，合理控制成本是重要的考量因素。本章将深入探讨 Claude API 的计费机制，以及如何在保证效率的前提下优化成本。

> **说明**：本章包含 Claude 4.5 系列的定价信息，实际价格请以官方文档为准。

## 26.1 计费机制详解

### 26.1.1 Token 计费模型

Claude API 采用基于 Token 的计费模型，分为输入 Token 和输出 Token。

**Claude 4.5 系列定价**：

| 模型 | 输入价格 (每百万Token) | 输出价格 (每百万Token) | 提示缓存（写入/读取） | 相对成本 |
|------|----------------------|----------------------|---------------------|---------|
| Claude Opus 4.5 | $5.00 | $25.00 | $6.25 / $0.50 | 最高 |
| Claude Sonnet 4.5 (≤200K) | $3.00 | $15.00 | $3.75 / $0.30 | 中等 |
| Claude Sonnet 4.5 (>200K) | $6.00 | $22.50 | $7.50 / $0.60 | 中高 |
| Claude Haiku 4.5 | $1.00 | $5.00 | $1.25 / $0.10 | 最低 |

> **注意**：Claude Sonnet 4.5 采用分层定价，上下文超过 200K Token 时价格翻倍。

**Claude 4 系列定价**：

| 模型 | 输入价格 (每百万Token) | 输出价格 (每百万Token) |
|------|----------------------|----------------------|
| Claude Opus 4 | $15.00 | $75.00 |
| Claude Sonnet 4 | $3.00 | $15.00 |

**Claude 3.5/3 系列定价**：

| 模型 | 输入价格 (每百万Token) | 输出价格 (每百万Token) |
|------|----------------------|----------------------|
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3.5 Haiku | $0.25 | $1.25 |
| Claude 3 Opus | $15.00 | $75.00 |
| Claude 3 Sonnet | $3.00 | $15.00 |
| Claude 3 Haiku | $0.25 | $1.25 |

### 26.1.2 Token 计算规则

Token 是 LLM 处理文本的基本单位，计算要点：

| 内容类型 | Token 估算 |
|---------|-----------|
| 英文 | 1 单词 ≈ 1.3 Token |
| 中文 | 1 汉字 ≈ 1.5-2 Token |
| 代码 | 变量名、符号各占 Token |
| 空白字符 | 空格、换行也计入 |

**估算示例**：
- 1000 个英文单词 ≈ 1300 Token
- 1000 个中文字符 ≈ 1500-2000 Token
- 100 行代码 ≈ 500-1500 Token（取决于代码密度）

### 26.1.3 成本估算工具

```typescript
// Token 估算工具
class TokenEstimator {
    // 粗略估算 Token 数量
    estimateTokens(text: string): number {
        const englishWords = text.match(/[a-zA-Z]+/g)?.length || 0;
        const chineseChars = text.match(/[\u4e00-\u9fa5]/g)?.length || 0;
        const others = text.match(/[0-9\W]/g)?.length || 0;
        
        return Math.ceil(
            englishWords * 1.3 +
            chineseChars * 1.8 +
            others * 0.5
        );
    }
    
    // 估算成本（美元）
    estimateCost(
        inputTokens: number,
        outputTokens: number,
        model: 'opus-4.5' | 'sonnet-4.5' | 'haiku-4.5'
    ): number {
        const pricing = {
            'opus-4.5': { input: 5, output: 25 },
            'sonnet-4.5': { input: 3, output: 15 },  // ≤200K Token
            'haiku-4.5': { input: 1, output: 5 }
        };
        
        const price = pricing[model];
        return (inputTokens * price.input + outputTokens * price.output) / 1000000;
    }
}
```

### 26.1.4 Claude Code 中查看成本

```bash
# 查看当前会话的 Token 使用情况
/usage

# 查看历史使用统计
claude usage --period month

# 设置成本预警
claude config set costAlert.daily 10  # 每日 $10 预警
claude config set costAlert.monthly 100  # 每月 $100 预警
```

## 26.2 模型选择策略

### 26.2.1 按任务选择模型

不同任务对模型能力的要求不同，合理选择可以显著降低成本：

| 任务类型 | 推荐模型 | 成本影响 |
|---------|---------|---------|
| 简单代码补全 | Haiku 4.5 | 最低 |
| 日常编码辅助 | Sonnet 4.5 | 中等 |
| 代码审查 | Sonnet 4.5 | 中等 |
| 复杂架构设计 | Opus 4.5 | 最高 |
| 长时间自主任务 | Opus 4.5 | 最高 |
| 批量代码生成 | Haiku 4.5 | 最低 |
| 文档生成 | Sonnet 4.5 / Haiku 4.5 | 中等/低 |

### 26.2.2 动态模型切换

```bash
# 配置默认模型（日常使用）
claude config set preferredModel claude-sonnet-4-5-20250929

# 临时使用高端模型（复杂任务）
claude --model claude-opus-4-5-20251124 "重构整个认证模块"

# 临时使用轻量模型（简单任务）
claude --model claude-haiku-4-5-20251015 "添加这个函数的注释"
```

### 26.2.3 成本对比示例

假设一个典型的开发会话：
- 输入：10,000 Token（代码上下文 + 提示）
- 输出：2,000 Token（生成的代码 + 解释）

| 模型 | 输入成本 | 输出成本 | 总成本 |
|------|---------|---------|--------|
| Opus 4.5 | $0.05 | $0.05 | $0.10 |
| Sonnet 4.5 | $0.03 | $0.03 | $0.06 |
| Haiku 4.5 | $0.01 | $0.01 | $0.02 |

**结论**：Sonnet 4.5 的成本约为 Opus 4.5 的 60%，Haiku 4.5 的成本约为 Sonnet 4.5 的 1/3。

## 26.3 上下文优化

### 26.3.1 精简上下文

上下文越长，成本越高。优化策略：

**只包含相关文件**：
```bash
# 不推荐：让 Claude 读取整个项目
> 分析这个项目的所有代码

# 推荐：指定相关文件
> 分析 src/auth/login.ts 和 src/auth/session.ts 的认证逻辑
```

**使用 .claudeignore**：
```
# .claudeignore
node_modules/
dist/
*.log
*.lock
coverage/
.git/
```

### 26.3.2 自动压缩配置

```bash
# 设置自动压缩阈值（Token 数）
claude config set autoCompactThreshold 50000

# 手动压缩当前会话
/compact
```

### 26.3.3 会话管理

```bash
# 开始新会话（清除上下文）
/clear

# 保存重要会话
/session save important-refactoring

# 恢复会话（避免重复上下文构建）
claude --resume important-refactoring
```

## 26.4 使用模式优化

### 26.4.1 批量处理

将多个小任务合并为一个大任务：

```bash
# 不推荐：多次小请求
> 给 function1 添加注释
> 给 function2 添加注释
> 给 function3 添加注释

# 推荐：一次批量请求
> 给 src/utils.ts 中的所有函数添加 JSDoc 注释
```

### 26.4.2 使用 Headless 模式

对于自动化任务，使用 Headless 模式更高效：

```bash
# 单次任务，避免交互开销
claude -p "为 src/api/ 下的所有文件生成单元测试" --output tests/

# 批量处理脚本
for file in src/components/*.tsx; do
    claude -p "为 $file 添加 PropTypes 验证" --model claude-haiku-4-5-20251015
done
```

### 26.4.3 缓存和复用

```bash
# 启用响应缓存
claude config set cache.enabled true
claude config set cache.ttl 3600  # 1小时

# 复用常见提示词
claude config set prompts.review "请审查以下代码的质量、安全性和性能"
```

## 26.5 企业成本管理

### 26.5.1 预算控制

```bash
# 设置团队预算
claude admin budget set --team engineering --monthly 1000

# 设置个人配额
claude admin quota set --user developer1 --daily 50

# 查看使用报告
claude admin report --period month --format csv > usage-report.csv
```

### 26.5.2 成本分配

```bash
# 按项目标记使用
claude --project frontend-v2 "实现用户登录功能"

# 查看项目成本
claude usage --by-project --period month
```

### 26.5.3 使用策略

| 策略 | 实施方法 | 预期节省 |
|------|---------|---------|
| 模型分层 | 简单任务用 Haiku，复杂任务用 Sonnet | 30-50% |
| 上下文优化 | 使用 .claudeignore，定期压缩 | 20-30% |
| 批量处理 | 合并小任务，使用脚本 | 10-20% |
| 缓存复用 | 启用缓存，复用提示词 | 5-15% |

## 26.6 成本监控

### 26.6.1 实时监控

```bash
# 查看实时使用情况
claude usage --realtime

# 设置预警通知
claude config set notifications.costAlert true
claude config set notifications.channel slack
claude config set notifications.webhook "https://hooks.slack.com/..."
```

### 26.6.2 使用报告

```bash
# 生成详细报告
claude usage report \
    --period 2025-11 \
    --by-model \
    --by-user \
    --format html \
    > november-report.html
```

### 26.6.3 成本分析

```typescript
// 成本分析脚本
import { ClaudeUsageAPI } from '@anthropic-ai/claude-code';

async function analyzeUsage() {
    const api = new ClaudeUsageAPI();
    const usage = await api.getUsage({
        period: 'month',
        groupBy: ['model', 'user', 'project']
    });
    
    // 找出成本最高的使用场景
    const topCosts = usage
        .sort((a, b) => b.cost - a.cost)
        .slice(0, 10);
    
    console.log('Top 10 Cost Centers:');
    topCosts.forEach((item, i) => {
        console.log(`${i + 1}. ${item.project} - ${item.user}: $${item.cost.toFixed(2)}`);
    });
}
```

## 26.7 成本优化案例

### 26.7.1 案例：代码审查优化

**优化前**：
- 使用 Opus 4.5 进行所有代码审查
- 每次审查包含完整文件历史
- 月成本：$500

**优化后**：
- 简单审查使用 Sonnet 4.5
- 只包含变更的代码
- 复杂审查才使用 Opus 4.5
- 月成本：$150（节省 70%）

### 26.7.2 案例：测试生成优化

**优化前**：
- 逐个文件生成测试
- 每次请求包含完整项目上下文
- 月成本：$200

**优化后**：
- 批量生成测试
- 使用 Haiku 4.5 生成基础测试
- 使用 Sonnet 4.5 优化复杂测试
- 月成本：$50（节省 75%）

## 26.8 本章小结

成本控制是 Claude Code 使用中的重要考量。通过合理的模型选择、上下文优化和使用模式调整，可以在保证效率的前提下显著降低成本。

---

**关键要点回顾**：

1. Claude 4.5 系列定价：Opus $5/$25，Sonnet $3/$15（≤200K）或 $6/$22.5（>200K），Haiku $1/$5（每百万 Token）
2. 按任务复杂度选择模型，简单任务用 Haiku，日常任务用 Sonnet，复杂任务用 Opus
3. 通过 .claudeignore、上下文压缩、批量处理等方式优化成本
4. 企业用户应建立预算控制、成本分配和监控机制
5. 合理优化可节省 50-70% 的成本
