# 第27章：性能调优指南

Claude Code 的性能直接影响开发效率。本章将探讨影响 Claude Code 性能的因素，以及如何通过各种手段优化响应速度和使用体验。

## 27.1 性能影响因素

### 27.1.1 响应时间构成

Claude Code 的响应时间由以下部分构成：

**总响应时间 = 网络延迟 + 请求处理时间 + 模型推理时间 + 响应传输时间**

```mermaid
flowchart LR
    A["网络延迟<br/>~50ms"] --> B["请求处理<br/>~10ms"]
    B --> C["模型推理<br/>变化大"]
    C --> D["响应传输<br/>变化大"]
```

### 27.1.2 影响因素分析

| 因素 | 影响程度 | 可控性 |
|------|---------|--------|
| 输入 Token 数量 | 高 | 高 |
| 输出 Token 数量 | 高 | 中 |
| 模型选择 | 高 | 高 |
| 网络条件 | 中 | 低 |
| API 负载 | 低 | 无 |

## 27.2 输入优化

### 27.2.1 精简提示词

```bash
# 冗长的提示词
claude "我现在正在开发一个电子商务网站，使用的是 React 框架，
版本是 18.2.0，配合 TypeScript 5.0 使用。我想请你帮我写一个
购物车组件，这个组件需要能够显示商品列表、计算总价、支持
数量修改和删除商品的功能。请使用函数式组件和 Hooks。"

# 精简的提示词
claude "React 18 + TS：创建购物车组件，功能：商品列表、总价计算、
数量修改、删除商品。使用函数组件 + Hooks。"
```

### 27.2.2 结构化输入

```bash
# 使用结构化格式减少歧义，提高处理效率
claude "任务：代码审查
文件：src/utils/validator.ts
重点：
1. 类型安全
2. 边界处理
3. 性能
输出：问题列表 + 修复建议"
```

### 27.2.3 上下文裁剪

```typescript
// 智能上下文裁剪
class ContextOptimizer {
    private readonly MAX_CONTEXT_TOKENS = 8000;
    
    optimizeContext(context: ConversationContext): ConversationContext {
        const totalTokens = this.estimateTokens(context);
        
        if (totalTokens <= this.MAX_CONTEXT_TOKENS) {
            return context;
        }
        
        // 策略1：移除旧消息
        const optimized = this.removeOldMessages(context);
        
        // 策略2：压缩长消息
        if (this.estimateTokens(optimized) > this.MAX_CONTEXT_TOKENS) {
            return this.compressLongMessages(optimized);
        }
        
        return optimized;
    }
    
    private removeOldMessages(context: ConversationContext): ConversationContext {
        const messages = [...context.messages];
        
        // 保留系统消息和最近的对话
        const systemMessages = messages.filter(m => m.role === 'system');
        const recentMessages = messages
            .filter(m => m.role !== 'system')
            .slice(-10);
        
        return {
            ...context,
            messages: [...systemMessages, ...recentMessages],
        };
    }
    
    private compressLongMessages(context: ConversationContext): ConversationContext {
        return {
            ...context,
            messages: context.messages.map(msg => {
                if (this.estimateTokens({ messages: [msg] }) > 1000) {
                    return {
                        ...msg,
                        content: this.summarize(msg.content),
                    };
                }
                return msg;
            }),
        };
    }
}
```

## 27.3 输出优化

### 27.3.1 限制输出长度

```bash
# 使用 max_tokens 限制输出
claude --max-tokens 500 "请简要解释什么是微服务架构"

# 在提示词中明确要求简洁
claude "用3句话解释微服务架构的核心概念"
```

### 27.3.2 流式输出

启用流式输出可以让用户更快看到响应：

```bash
# 默认启用流式输出
claude "生成一个 Node.js Express 服务器模板"

# 如需完整响应后再显示
claude --no-stream "生成一个 Node.js Express 服务器模板"
```

### 27.3.3 指定输出格式

```bash
# 指定简洁的输出格式
claude "列出 React Hooks 的使用规则，使用编号列表，每条不超过20字"

# 指定结构化输出
claude "分析这段代码的问题，输出 JSON 格式：
{\"issues\": [{\"line\": number, \"severity\": string, \"message\": string}]}"
```

## 27.4 模型选择优化

### 27.4.1 任务-模型匹配

```typescript
// 智能模型选择器
class ModelSelector {
    selectModel(task: TaskDescription): string {
        // 简单任务使用 Haiku
        if (this.isSimpleTask(task)) {
            return 'claude-3-haiku';
        }
        
        // 复杂推理任务使用 Opus
        if (this.isComplexReasoning(task)) {
            return 'claude-3-opus';
        }
        
        // 默认使用 Sonnet
        return 'claude-3-sonnet';
    }
    
    private isSimpleTask(task: TaskDescription): boolean {
        const simplePatterns = [
            /格式化/,
            /简单解释/,
            /翻译/,
            /拼写检查/,
            /语法修正/,
        ];
        return simplePatterns.some(p => p.test(task.description));
    }
    
    private isComplexReasoning(task: TaskDescription): boolean {
        const complexPatterns = [
            /架构设计/,
            /性能优化/,
            /安全审计/,
            /复杂算法/,
            /系统分析/,
        ];
        return complexPatterns.some(p => p.test(task.description));
    }
}
```

### 27.4.2 模型性能对比

| 模型 | 平均响应时间 | 适用场景 |
|------|-------------|---------|
| Haiku | ~1-3秒 | 简单查询、格式化、翻译 |
| Sonnet | ~3-10秒 | 代码生成、审查、一般开发 |
| Opus | ~10-30秒 | 复杂架构、深度分析 |

## 27.5 网络优化

### 27.5.1 连接复用

```typescript
// HTTP 连接池配置
import { Agent } from 'https';

const agent = new Agent({
    keepAlive: true,
    keepAliveMsecs: 30000,
    maxSockets: 10,
    maxFreeSockets: 5,
});

// 使用连接池
const response = await fetch('https://api.anthropic.com/v1/messages', {
    agent,
    // ... 其他配置
});
```

### 27.5.2 请求重试策略

```typescript
// 指数退避重试
class RetryHandler {
    private readonly maxRetries = 3;
    private readonly baseDelay = 1000;
    
    async executeWithRetry<T>(fn: () => Promise<T>): Promise<T> {
        let lastError: Error;
        
        for (let attempt = 0; attempt < this.maxRetries; attempt++) {
            try {
                return await fn();
            } catch (error) {
                lastError = error;
                
                if (!this.isRetryable(error)) {
                    throw error;
                }
                
                const delay = this.baseDelay * Math.pow(2, attempt);
                await this.sleep(delay);
            }
        }
        
        throw lastError;
    }
    
    private isRetryable(error: any): boolean {
        // 网络错误、超时、5xx 错误可重试
        return (
            error.code === 'ECONNRESET' ||
            error.code === 'ETIMEDOUT' ||
            (error.status >= 500 && error.status < 600)
        );
    }
    
    private sleep(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
```

## 27.6 并发与批处理

### 27.6.1 并发请求

```typescript
// 并发请求管理器
class ConcurrentRequestManager {
    private readonly maxConcurrent = 5;
    private activeRequests = 0;
    private queue: Array<() => Promise<void>> = [];
    
    async execute<T>(fn: () => Promise<T>): Promise<T> {
        return new Promise((resolve, reject) => {
            const task = async () => {
                try {
                    const result = await fn();
                    resolve(result);
                } catch (error) {
                    reject(error);
                } finally {
                    this.activeRequests--;
                    this.processQueue();
                }
            };
            
            if (this.activeRequests < this.maxConcurrent) {
                this.activeRequests++;
                task();
            } else {
                this.queue.push(task);
            }
        });
    }
    
    private processQueue(): void {
        if (this.queue.length > 0 && this.activeRequests < this.maxConcurrent) {
            const task = this.queue.shift();
            this.activeRequests++;
            task();
        }
    }
}

// 使用示例
const manager = new ConcurrentRequestManager();

const results = await Promise.all(
    files.map(file => 
        manager.execute(() => claude.analyze(file))
    )
);
```

### 27.6.2 批量处理

```bash
# 批量处理多个文件
claude "请分析以下文件的代码质量：
1. src/utils/helper.ts
2. src/services/user.ts
3. src/controllers/auth.ts

对每个文件输出：文件名、问题数量、主要问题"
```

## 27.7 性能监控

### 27.7.1 性能指标收集

```typescript
// 性能监控
class PerformanceMonitor {
    private metrics: PerformanceMetrics[] = [];
    
    async measureRequest<T>(
        name: string,
        fn: () => Promise<T>
    ): Promise<T> {
        const startTime = performance.now();
        const startMemory = process.memoryUsage().heapUsed;
        
        try {
            const result = await fn();
            
            this.recordMetrics({
                name,
                duration: performance.now() - startTime,
                memoryDelta: process.memoryUsage().heapUsed - startMemory,
                success: true,
                timestamp: new Date(),
            });
            
            return result;
        } catch (error) {
            this.recordMetrics({
                name,
                duration: performance.now() - startTime,
                memoryDelta: process.memoryUsage().heapUsed - startMemory,
                success: false,
                error: error.message,
                timestamp: new Date(),
            });
            throw error;
        }
    }
    
    getStatistics(): PerformanceStatistics {
        const durations = this.metrics.map(m => m.duration);
        
        return {
            count: this.metrics.length,
            avgDuration: this.average(durations),
            p50Duration: this.percentile(durations, 50),
            p95Duration: this.percentile(durations, 95),
            p99Duration: this.percentile(durations, 99),
            successRate: this.metrics.filter(m => m.success).length / this.metrics.length,
        };
    }
}
```

## 27.8 本章小结

本章详细介绍了 Claude Code 的性能调优方法：

1. **输入优化**：精简提示词、结构化输入、上下文裁剪
2. **输出优化**：限制长度、流式输出、指定格式
3. **模型选择**：根据任务复杂度选择合适模型
4. **网络优化**：连接复用、重试策略
5. **并发处理**：并发请求管理、批量处理
6. **性能监控**：指标收集、统计分析

性能优化的核心原则：
- 减少不必要的 Token 传输
- 选择合适的模型
- 利用并发提高吞吐量
- 持续监控发现瓶颈
