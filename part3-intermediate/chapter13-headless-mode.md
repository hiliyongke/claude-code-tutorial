# 第13章：Headless 模式与脚本集成

## 13.1 Headless 模式概述

Headless 模式允许在非交互环境中使用 Claude Code，这对于自动化脚本、CI/CD 流程和批处理任务至关重要。

### 13.1.1 什么是 Headless 模式

Headless 模式是指 Claude Code 在没有用户交互的情况下运行：

- 不需要用户实时输入
- 不显示交互式界面
- 通过参数或标准输入接收指令
- 输出可以被程序解析

### 13.1.2 适用场景

| 场景 | 描述 | 示例 |
|------|------|------|
| CI/CD | 自动化构建和部署流程 | 代码审查、测试生成 |
| 批处理 | 批量处理多个文件 | 批量添加注释、格式化 |
| 定时任务 | 定期执行的自动化任务 | 日报生成、代码分析 |
| 管道处理 | 与其他命令组合 | 日志分析、数据转换 |
| 脚本集成 | 嵌入到 Shell/Python 脚本 | 自动化工作流 |

### 13.1.3 基本语法

```bash
# 使用 -p 参数传入提示词
claude -p "你的问题或指令"

# 从标准输入读取
echo "你的问题" | claude --stdin

# 组合使用
cat file.txt | claude --stdin -p "分析这个文件"
```

## 13.2 命令行参数详解

### 13.2.1 输入相关参数

**-p, --prompt**

直接传入提示词：

```bash
# 简单查询
claude -p "什么是 Docker?"

# 多行提示词（使用引号）
claude -p "请解释以下概念：
1. 容器
2. 镜像
3. 仓库"

# 使用变量
QUESTION="如何优化 Node.js 性能?"
claude -p "$QUESTION"
```

**--stdin**

从标准输入读取：

```bash
# 管道输入
echo "解释这段代码" | claude --stdin

# 文件内容
cat src/index.js | claude --stdin -p "审查这段代码"

# Here Document
claude --stdin << EOF
请分析以下需求：
1. 用户注册功能
2. 邮箱验证
3. 密码重置
EOF
```

**-f, --file**

指定输入文件：

```bash
# 单个文件
claude -f src/index.js -p "解释这个文件"

# 多个文件
claude -f src/auth.js -f src/user.js -p "这两个模块如何交互?"

# 通配符（需要 shell 展开）
claude -f src/*.ts -p "分析这些 TypeScript 文件"
```

### 13.2.2 输出相关参数

**-o, --output**

输出到文件：

```bash
# 保存到文件
claude -p "生成 README 模板" -o README.md

# 指定路径
claude -p "生成配置文件" -o ./config/app.config.js
```

**--output-format**

指定输出格式：

```bash
# 纯文本（默认）
claude -p "列出 Git 命令" --output-format text

# JSON 格式
claude -p "分析项目结构" --output-format json

# Markdown 格式
claude -p "生成文档" --output-format markdown
```

**--no-stream**

禁用流式输出：

```bash
# 等待完整响应
claude -p "生成长文档" --no-stream
```

**-q, --quiet**

静默模式：

```bash
# 只输出核心结果
claude -p "计算 1+1" --quiet
```

### 13.2.3 行为控制参数

**--yes, -y**

自动确认所有操作：

```bash
# 自动确认（谨慎使用）
claude -p "修复所有 lint 错误" --yes
```

**--no-confirm**

禁用特定确认：

```bash
# 禁用文件操作确认
claude -p "格式化代码" --no-confirm file
```

**--timeout**

设置超时时间：

```bash
# 60 秒超时
claude -p "复杂分析任务" --timeout 60000
```

**--max-turns**

限制对话轮次：

```bash
# 最多 5 轮对话
claude -p "实现功能" --max-turns 5
```

## 13.3 Shell 脚本集成

### 13.3.1 基础脚本示例

**代码审查脚本**：

```bash
#!/bin/bash
# review.sh - 自动代码审查脚本

set -e

# 获取变更的文件
CHANGED_FILES=$(git diff --name-only HEAD~1 -- '*.js' '*.ts')

if [ -z "$CHANGED_FILES" ]; then
    echo "没有需要审查的文件"
    exit 0
fi

echo "正在审查以下文件："
echo "$CHANGED_FILES"

# 对每个文件进行审查
for file in $CHANGED_FILES; do
    echo "审查: $file"
    
    claude -f "$file" \
        -p "审查这段代码，关注安全性和性能问题" \
        --output-format markdown \
        -o "reviews/${file}.review.md" \
        --quiet
done

echo "审查完成，结果保存在 reviews/ 目录"
```

**批量文档生成脚本**：

```bash
#!/bin/bash
# generate-docs.sh - 批量生成 API 文档

set -e

# 查找所有 Controller 文件
CONTROLLERS=$(find src/controllers -name "*Controller.ts")

for controller in $CONTROLLERS; do
    # 提取控制器名称
    name=$(basename "$controller" .ts)
    
    echo "生成文档: $name"
    
    claude -f "$controller" \
        -p "为这个控制器生成 API 文档，使用 Markdown 格式，包含：
            - 端点列表
            - 请求参数
            - 响应格式
            - 示例" \
        -o "docs/api/${name}.md" \
        --quiet
done

echo "文档生成完成"
```

### 13.3.2 错误处理

```bash
#!/bin/bash
# safe-claude.sh - 带错误处理的 Claude 调用

set -e

# 函数：安全调用 Claude
safe_claude() {
    local prompt="$1"
    local output_file="$2"
    local max_retries=3
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        if claude -p "$prompt" -o "$output_file" --quiet 2>/dev/null; then
            return 0
        fi
        
        retry_count=$((retry_count + 1))
        echo "重试 $retry_count/$max_retries..."
        sleep 2
    done
    
    echo "错误：Claude 调用失败" >&2
    return 1
}

# 使用
if safe_claude "生成测试用例" "tests/generated.test.js"; then
    echo "成功生成测试用例"
else
    echo "生成失败"
    exit 1
fi
```

### 13.3.3 并行处理

```bash
#!/bin/bash
# parallel-review.sh - 并行代码审查

set -e

# 最大并行数
MAX_PARALLEL=4

# 审查单个文件的函数
review_file() {
    local file="$1"
    local output="reviews/$(basename "$file").review.md"
    
    claude -f "$file" \
        -p "审查代码质量" \
        -o "$output" \
        --quiet
    
    echo "完成: $file"
}

export -f review_file

# 使用 xargs 并行执行
find src -name "*.ts" | xargs -P $MAX_PARALLEL -I {} bash -c 'review_file "$@"' _ {}

echo "所有审查完成"
```

## 13.4 管道操作

### 13.4.1 基础管道

```bash
# Git diff 审查
git diff HEAD~1 | claude --stdin -p "审查这些代码变更"

# 日志分析
tail -100 /var/log/app.log | claude --stdin -p "分析错误模式"

# 命令输出处理
npm audit | claude --stdin -p "总结安全漏洞并给出修复建议"
```

### 13.4.2 链式管道

```bash
# 代码 -> 分析 -> 格式化
cat src/complex.js | \
    claude --stdin -p "简化这段代码" | \
    prettier --stdin-filepath temp.js

# 多步骤处理
git log --oneline -20 | \
    claude --stdin -p "总结最近的提交" --output-format json | \
    jq '.summary'
```

### 13.4.3 与常用工具组合

**与 jq 组合**：

```bash
# 提取 JSON 响应中的特定字段
claude -p "分析项目依赖" --output-format json | jq '.dependencies[]'
```

**与 grep 组合**：

```bash
# 过滤输出
claude -p "列出所有 TODO 项" | grep -E "^\d+\."
```

**与 awk 组合**：

```bash
# 处理表格输出
claude -p "列出文件大小" | awk '{print $1, $2}'
```

## 13.5 Python 脚本集成

### 13.5.1 基础集成

```python
#!/usr/bin/env python3
"""claude_helper.py - Python 集成示例"""

import subprocess
import json
from typing import Optional

def call_claude(
    prompt: str,
    files: Optional[list] = None,
    output_format: str = "text",
    timeout: int = 60
) -> str:
    """调用 Claude Code"""
    
    cmd = ["claude", "-p", prompt, "--output-format", output_format, "--quiet"]
    
    if files:
        for f in files:
            cmd.extend(["-f", f])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode != 0:
            raise Exception(f"Claude 调用失败: {result.stderr}")
        
        return result.stdout.strip()
    
    except subprocess.TimeoutExpired:
        raise Exception("Claude 调用超时")


def analyze_code(file_path: str) -> dict:
    """分析代码文件"""
    
    prompt = """分析这个代码文件，返回 JSON 格式：
    {
        "complexity": "low/medium/high",
        "issues": ["问题1", "问题2"],
        "suggestions": ["建议1", "建议2"]
    }"""
    
    response = call_claude(prompt, files=[file_path], output_format="json")
    return json.loads(response)


def generate_tests(file_path: str, output_path: str) -> None:
    """生成测试用例"""
    
    prompt = "为这个文件生成单元测试，使用 Jest 框架"
    
    tests = call_claude(prompt, files=[file_path])
    
    with open(output_path, "w") as f:
        f.write(tests)


# 使用示例
if __name__ == "__main__":
    # 分析代码
    analysis = analyze_code("src/services/UserService.ts")
    print(f"复杂度: {analysis['complexity']}")
    print(f"问题: {analysis['issues']}")
    
    # 生成测试
    generate_tests(
        "src/services/UserService.ts",
        "tests/UserService.test.ts"
    )
```

### 13.5.2 批量处理

```python
#!/usr/bin/env python3
"""batch_process.py - 批量处理脚本"""

import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_file(file_path: Path) -> dict:
    """处理单个文件"""
    
    result = subprocess.run(
        [
            "claude", "-f", str(file_path),
            "-p", "添加 JSDoc 注释",
            "--quiet"
        ],
        capture_output=True,
        text=True
    )
    
    return {
        "file": str(file_path),
        "success": result.returncode == 0,
        "output": result.stdout if result.returncode == 0 else result.stderr
    }


def batch_process(directory: str, pattern: str = "*.ts", max_workers: int = 4):
    """批量处理目录中的文件"""
    
    files = list(Path(directory).rglob(pattern))
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, f): f for f in files}
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            status = "✓" if result["success"] else "✗"
            print(f"{status} {result['file']}")
    
    # 统计
    success_count = sum(1 for r in results if r["success"])
    print(f"\n完成: {success_count}/{len(results)} 成功")
    
    return results


if __name__ == "__main__":
    batch_process("src", "*.ts")
```

### 13.5.3 交互式脚本

```python
#!/usr/bin/env python3
"""interactive_claude.py - 交互式 Claude 脚本"""

import subprocess
import sys

def interactive_session():
    """启动交互式会话"""
    
    print("Claude 交互式会话 (输入 'exit' 退出)")
    print("-" * 40)
    
    history = []
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() == "exit":
                break
            
            if not user_input:
                continue
            
            # 构建带历史的提示词
            context = "\n".join(history[-5:])  # 保留最近 5 条
            prompt = f"{context}\n\n用户: {user_input}" if context else user_input
            
            # 调用 Claude
            result = subprocess.run(
                ["claude", "-p", prompt, "--quiet"],
                capture_output=True,
                text=True
            )
            
            response = result.stdout.strip()
            print(f"\nClaude: {response}")
            
            # 更新历史
            history.append(f"用户: {user_input}")
            history.append(f"Claude: {response}")
            
        except KeyboardInterrupt:
            print("\n\n会话结束")
            break


if __name__ == "__main__":
    interactive_session()
```

## 13.6 CI/CD 集成

### 13.6.1 GitHub Actions

```yaml
# .github/workflows/code-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-cli
      
      - name: Configure Claude
        run: |
          mkdir -p ~/.config/claude
          echo '{"apiKey": "${{ secrets.ANTHROPIC_API_KEY }}"}' > ~/.config/claude/config.json
      
      - name: Get changed files
        id: changed
        run: |
          FILES=$(git diff --name-only ${{ github.event.pull_request.base.sha }} -- '*.ts' '*.js')
          echo "files=$FILES" >> $GITHUB_OUTPUT
      
      - name: Run code review
        if: steps.changed.outputs.files != ''
        run: |
          for file in ${{ steps.changed.outputs.files }}; do
            echo "Reviewing: $file"
            claude -f "$file" \
              -p "审查这段代码，指出问题和改进建议，格式为 Markdown" \
              --quiet >> review-comments.md
          done
      
      - name: Post review comment
        if: steps.changed.outputs.files != ''
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review-comments.md', 'utf8');
            
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## AI Code Review\n\n${review}`
            });
```

### 13.6.2 GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - review
  - test

ai-code-review:
  stage: review
  image: node:20
  
  before_script:
    - npm install -g @anthropic-ai/claude-cli
    - mkdir -p ~/.config/claude
    - echo "{\"apiKey\": \"$ANTHROPIC_API_KEY\"}" > ~/.config/claude/config.json
  
  script:
    - |
      # 获取 MR 变更的文件
      CHANGED_FILES=$(git diff --name-only $CI_MERGE_REQUEST_DIFF_BASE_SHA -- '*.ts' '*.js')
      
      if [ -n "$CHANGED_FILES" ]; then
        for file in $CHANGED_FILES; do
          echo "Reviewing: $file"
          claude -f "$file" -p "审查代码" --quiet >> review.md
        done
      fi
  
  artifacts:
    paths:
      - review.md
    expire_in: 1 week
  
  only:
    - merge_requests
```

### 13.6.3 Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        ANTHROPIC_API_KEY = credentials('anthropic-api-key')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'npm install -g @anthropic-ai/claude-cli'
                sh '''
                    mkdir -p ~/.config/claude
                    echo "{\\"apiKey\\": \\"${ANTHROPIC_API_KEY}\\"}" > ~/.config/claude/config.json
                '''
            }
        }
        
        stage('Code Review') {
            steps {
                script {
                    def changedFiles = sh(
                        script: "git diff --name-only HEAD~1 -- '*.ts' '*.js'",
                        returnStdout: true
                    ).trim()
                    
                    if (changedFiles) {
                        changedFiles.split('\n').each { file ->
                            sh """
                                claude -f "${file}" \
                                    -p "审查代码质量" \
                                    --quiet >> review-report.md
                            """
                        }
                    }
                }
            }
        }
        
        stage('Publish Report') {
            steps {
                archiveArtifacts artifacts: 'review-report.md'
            }
        }
    }
}
```

## 13.7 定时任务

### 13.7.1 Cron 任务

```bash
# 编辑 crontab
crontab -e

# 每天早上 9 点生成代码质量报告
0 9 * * * /home/user/scripts/daily-report.sh >> /var/log/claude-report.log 2>&1

# 每周一生成周报
0 10 * * 1 /home/user/scripts/weekly-summary.sh >> /var/log/claude-weekly.log 2>&1
```

**daily-report.sh**：

```bash
#!/bin/bash
# daily-report.sh - 每日代码质量报告

cd /path/to/project

# 生成报告
claude -p "分析 src/ 目录的代码质量，生成报告包含：
1. 代码复杂度统计
2. 潜在问题列表
3. 改进建议
格式：Markdown" \
    --cwd . \
    -o "reports/daily-$(date +%Y%m%d).md" \
    --quiet

# 发送邮件通知
if [ -f "reports/daily-$(date +%Y%m%d).md" ]; then
    mail -s "每日代码质量报告" team@company.com < "reports/daily-$(date +%Y%m%d).md"
fi
```

### 13.7.2 系统服务

```ini
# /etc/systemd/system/claude-monitor.service
[Unit]
Description=Claude Code Monitor
After=network.target

[Service]
Type=simple
User=developer
WorkingDirectory=/home/developer/project
ExecStart=/home/developer/scripts/monitor.sh
Restart=always
RestartSec=3600

[Install]
WantedBy=multi-user.target
```

## 13.8 本章小结

Headless 模式是 Claude Code 在自动化场景中的核心能力。通过命令行参数、管道操作和脚本集成，可以将 Claude Code 融入到各种自动化工作流中。

在下一部分中，我们将进入高级篇，深入探讨 Hooks、Skills、Spec 和 MCP 等高级功能。

---

**关键要点回顾**：

1. 使用 `-p` 参数传入提示词实现非交互执行
2. `--stdin` 支持管道输入
3. `--output-format` 控制输出格式便于程序解析
4. 可与 Shell、Python 脚本深度集成
5. 支持 CI/CD 流程和定时任务

**自动化检查清单**：

- [ ] 设置适当的超时时间
- [ ] 添加错误处理和重试机制
- [ ] 使用 `--quiet` 减少不必要的输出
- [ ] 保护 API 密钥安全
- [ ] 记录日志便于问题排查
