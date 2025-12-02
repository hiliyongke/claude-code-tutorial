# 第15章：Skills 能力扩展系统

## 15.1 Skills 系统概述

Skills 是 Claude Code 的能力扩展机制，允许用户封装特定领域的知识、工具和工作流，实现能力的模块化和复用。

### 应用场景速览

在深入学习 Skills 之前，先看看它能解决哪些实际问题：

| 场景 | 问题 | Skills 解决方案 |
|------|------|----------------|
| 框架开发 | 每次都要向 Claude 解释 React/Vue 的最佳实践 | 使用 `react-developer` Skill 预置专业知识 |
| 团队规范 | 新成员不了解团队的代码规范 | 创建项目 Skill 封装团队规范 |
| 重复工作 | 经常需要创建相似的组件/模块结构 | 在 Skill 中定义模板和自动化工具 |
| 知识沉淀 | 项目特有的领域知识难以传承 | 将领域知识封装为 Skill 分享给团队 |
| 工作流标准化 | 不同成员的开发流程不一致 | 通过 Skill 统一工作流程 |

**典型使用示例**：

```bash
# 场景：使用 React 专家 Skill 开发前端
claude --skill react-developer

> 创建一个用户列表组件，支持分页和搜索

# Claude 会按照 React 最佳实践生成代码：
# - 使用函数组件 + Hooks
# - 完整的 TypeScript 类型定义
# - 符合团队代码规范
# - 自动创建测试文件
```

> **提示**：本章将详细讲解如何使用和创建 Skills，并在 15.5 节提供最佳实践指南。

### 15.1.1 什么是 Skills

Skills 可以理解为 Claude 的"技能包"：

- **知识封装**：特定领域的专业知识
- **工具集成**：预配置的工具组合
- **工作流定义**：标准化的操作流程
- **提示词模板**：优化的提示词集合

### 15.1.2 Skills 的价值

**Skills 的核心价值**：

| 价值 | 说明 |
|------|------|
| 复用性 | 一次创建，多处使用 |
| 一致性 | 团队统一的工作方式 |
| 专业性 | 封装领域专家知识 |
| 可分享 | 团队或社区共享 |

### 15.1.3 Skills 类型

| 类型 | 描述 | 示例 |
|------|------|------|
| 官方 Skills | Anthropic 提供的官方技能 | 代码审查、测试生成 |
| 社区 Skills | 社区贡献的技能 | 框架特定技能 |
| 项目 Skills | 项目级自定义技能 | 项目规范、工作流 |
| 用户 Skills | 个人自定义技能 | 个人偏好、常用操作 |

## 15.2 Skills 结构

### 15.2.1 目录结构

一个完整的 Skill 包含以下结构：

```
my-skill/
├── skill.json          # Skill 元数据
├── README.md           # 使用说明
├── prompts/            # 提示词模板
│   ├── main.md         # 主提示词
│   └── templates/      # 子模板
│       ├── review.md
│       └── generate.md
├── tools/              # 自定义工具
│   └── custom-tool.js
├── hooks/              # Skill 专用 Hooks
│   └── post-generate.sh
└── examples/           # 使用示例
    └── example.md
```

### 15.2.2 skill.json 配置

```json
{
  "name": "react-developer",
  "version": "1.0.0",
  "description": "React 开发专家技能包",
  "author": "Your Name",
  "license": "MIT",
  
  "keywords": ["react", "frontend", "typescript"],
  
  "dependencies": {
    "node": ">=18.0.0"
  },
  
  "prompts": {
    "main": "prompts/main.md",
    "templates": {
      "component": "prompts/templates/component.md",
      "hook": "prompts/templates/hook.md",
      "test": "prompts/templates/test.md"
    }
  },
  
  "tools": [
    {
      "name": "create-component",
      "script": "tools/create-component.js"
    }
  ],
  
  "hooks": [
    {
      "event": "PostToolUse",
      "match": {"tool": "Write"},
      "script": "hooks/format-code.sh"
    }
  ],
  
  "config": {
    "componentStyle": "functional",
    "stateManagement": "hooks",
    "testFramework": "jest"
  }
}
```

### 15.2.3 主提示词文件

```markdown
<!-- prompts/main.md -->

# React 开发专家

你是一个专业的 React 开发专家，精通以下技术：

## 核心技能

- React 18+ 函数组件和 Hooks
- TypeScript 类型系统
- 状态管理（useState, useReducer, Zustand, Redux）
- 性能优化（memo, useMemo, useCallback）
- 测试（Jest, React Testing Library）

## 开发规范

### 组件设计原则

1. **单一职责**：每个组件只做一件事
2. **组合优于继承**：使用组合模式构建复杂组件
3. **Props 类型定义**：所有 props 必须有 TypeScript 接口
4. **默认值处理**：使用解构默认值或 defaultProps

### 代码风格

- 使用函数组件，避免类组件
- 使用 named exports，避免 default exports
- 组件文件名使用 PascalCase
- Hook 文件名使用 camelCase，以 use 开头

### 目录组织

```
src/
├── components/     # 通用组件
├── features/       # 功能模块
├── hooks/          # 自定义 Hooks
├── utils/          # 工具函数
└── types/          # 类型定义
```

## 可用模板

使用以下命令调用模板：

- `/template component` - 创建组件
- `/template hook` - 创建自定义 Hook
- `/template test` - 创建测试文件
```

## 15.3 创建自定义 Skills

### 15.3.1 初始化 Skill

```bash
# 创建 Skill 目录
mkdir my-skill && cd my-skill

# 初始化
claude skills init

# 或手动创建结构
mkdir -p prompts/templates tools hooks examples
```

### 15.3.2 编写提示词

**主提示词 (prompts/main.md)**：

```markdown
# [Skill 名称]

## 角色定义

你是一个专业的 [领域] 专家，具备以下能力：

- [能力 1]
- [能力 2]
- [能力 3]

## 工作原则

1. [原则 1]
2. [原则 2]
3. [原则 3]

## 输出规范

### 代码规范

- [规范 1]
- [规范 2]

### 文档规范

- [规范 1]
- [规范 2]

## 常用操作

### 操作 1：[名称]

[操作说明]

### 操作 2：[名称]

[操作说明]
```

**模板提示词 (prompts/templates/component.md)**：

```markdown
# 组件创建模板

请根据以下要求创建 React 组件：

## 组件信息

- 名称：{{name}}
- 类型：{{type}}
- 描述：{{description}}

## 要求

1. 使用 TypeScript
2. 定义完整的 Props 接口
3. 添加 JSDoc 注释
4. 包含基础样式

## 输出格式

```tsx
// {{name}}.tsx

interface {{name}}Props {
  // props 定义
}

export const {{name}}: React.FC<{{name}}Props> = (props) => {
  // 组件实现
};
```
```

### 15.3.3 添加自定义工具

```javascript
// tools/create-component.js

module.exports = {
  name: 'create-component',
  description: '创建 React 组件文件结构',
  
  inputSchema: {
    type: 'object',
    properties: {
      name: {
        type: 'string',
        description: '组件名称'
      },
      path: {
        type: 'string',
        description: '目标路径'
      },
      withTest: {
        type: 'boolean',
        description: '是否创建测试文件',
        default: true
      },
      withStyles: {
        type: 'boolean',
        description: '是否创建样式文件',
        default: true
      }
    },
    required: ['name']
  },
  
  async execute(params, context) {
    const { name, path = 'src/components', withTest, withStyles } = params;
    const componentDir = `${path}/${name}`;
    
    // 创建目录
    await context.tools.mkdir(componentDir);
    
    // 创建组件文件
    const componentContent = generateComponentTemplate(name);
    await context.tools.write(`${componentDir}/${name}.tsx`, componentContent);
    
    // 创建 index 文件
    await context.tools.write(
      `${componentDir}/index.ts`,
      `export { ${name} } from './${name}';\n`
    );
    
    // 创建测试文件
    if (withTest) {
      const testContent = generateTestTemplate(name);
      await context.tools.write(`${componentDir}/${name}.test.tsx`, testContent);
    }
    
    // 创建样式文件
    if (withStyles) {
      await context.tools.write(`${componentDir}/${name}.module.css`, '');
    }
    
    return {
      success: true,
      files: [
        `${componentDir}/${name}.tsx`,
        `${componentDir}/index.ts`,
        withTest && `${componentDir}/${name}.test.tsx`,
        withStyles && `${componentDir}/${name}.module.css`
      ].filter(Boolean)
    };
  }
};

function generateComponentTemplate(name) {
  return `import React from 'react';
import styles from './${name}.module.css';

interface ${name}Props {
  children?: React.ReactNode;
}

export const ${name}: React.FC<${name}Props> = ({ children }) => {
  return (
    <div className={styles.container}>
      {children}
    </div>
  );
};
`;
}

function generateTestTemplate(name) {
  return `import { render, screen } from '@testing-library/react';
import { ${name} } from './${name}';

describe('${name}', () => {
  it('renders children', () => {
    render(<${name}>Test</${name}>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
});
`;
}
```

### 15.3.4 配置 Hooks

```bash
#!/bin/bash
# hooks/format-code.sh

TOOL_NAME="$1"
PARAMS="$2"

if [ "$TOOL_NAME" == "Write" ]; then
    PATH=$(echo "$PARAMS" | jq -r '.path')
    
    # 格式化 TypeScript/JavaScript 文件
    if [[ "$PATH" == *.ts ]] || [[ "$PATH" == *.tsx ]] || \
       [[ "$PATH" == *.js ]] || [[ "$PATH" == *.jsx ]]; then
        npx prettier --write "$PATH" 2>/dev/null
        npx eslint --fix "$PATH" 2>/dev/null
    fi
fi
```

## 15.4 使用 Skills

### 15.4.1 安装 Skills

```bash
# 从官方仓库安装
claude skills install @anthropic/react-developer

# 从 GitHub 安装
claude skills install github:username/skill-name

# 从本地路径安装
claude skills install ./path/to/skill

# 安装特定版本
claude skills install @anthropic/react-developer@1.2.0
```

### 15.4.2 激活 Skills

```bash
# 在会话中激活
claude --skill react-developer

# 激活多个 Skills
claude --skill react-developer --skill testing-expert

# 在配置中默认激活
# ~/.config/claude/config.json
{
  "defaultSkills": ["react-developer"]
}
```

### 15.4.3 在会话中使用

```
> /skill react-developer

已激活 Skill: react-developer
可用命令：
- /template component - 创建组件
- /template hook - 创建 Hook
- /template test - 创建测试

> /template component
请提供组件信息：
- 名称：UserProfile
- 类型：展示组件
- 描述：显示用户个人信息

[使用模板生成组件]
```

### 15.4.4 管理 Skills

```bash
# 列出已安装的 Skills
claude skills list

# 查看 Skill 详情
claude skills info react-developer

# 更新 Skill
claude skills update react-developer

# 卸载 Skill
claude skills uninstall react-developer

# 查看可用的官方 Skills
claude skills search react
```

## 15.5 Skills 开发最佳实践

### 15.5.1 提示词设计

**清晰的角色定义**：

```markdown
# 角色定义

你是一个专业的 [具体角色]，专注于 [具体领域]。

## 核心能力
- [能力 1]：[详细说明]
- [能力 2]：[详细说明]

## 工作边界
- 擅长：[列举擅长的事项]
- 不擅长：[列举不擅长的事项，引导用户使用其他 Skill]
```

**具体的规范说明**：

```markdown
## 代码规范

### 命名规范
| 类型 | 规范 | 示例 |
|------|------|------|
| 组件 | PascalCase | UserProfile |
| Hook | camelCase + use 前缀 | useUserData |
| 工具函数 | camelCase | formatDate |
| 常量 | UPPER_SNAKE_CASE | MAX_RETRY_COUNT |

### 文件组织
- 每个组件一个目录
- index.ts 只用于导出
- 测试文件与源文件同目录
```

### 15.5.2 模板设计

**使用变量占位符**：

```markdown
# {{templateName}} 模板

## 输入变量
- `{{varName}}`: {{description}}

## 生成内容

```{{language}}
// {{fileName}}

{{generatedCode}}
```
```

**提供多种变体**：

```markdown
## 组件模板变体

### 1. 基础组件
适用于简单的展示组件

### 2. 带状态组件
适用于需要内部状态的组件

### 3. 容器组件
适用于数据获取和逻辑处理

请选择适合的变体：
```

### 15.5.3 工具设计

**单一职责**：

```javascript
// 好：单一职责
module.exports = {
  name: 'create-component',
  // 只负责创建组件
};

// 不好：职责过多
module.exports = {
  name: 'create-and-test-and-deploy',
  // 做太多事情
};
```

**完善的错误处理**：

```javascript
async execute(params, context) {
  try {
    // 参数验证
    if (!params.name) {
      return { error: '缺少必需参数: name' };
    }
    
    // 执行操作
    const result = await doSomething(params);
    
    return { success: true, data: result };
    
  } catch (error) {
    return { 
      error: `操作失败: ${error.message}`,
      details: error.stack
    };
  }
}
```

### 15.5.4 文档编写

**README.md 模板**：

```markdown
# Skill 名称

简短描述

## 安装

```bash
claude skills install skill-name
```

## 功能特性

- 特性 1
- 特性 2

## 快速开始

```bash
claude --skill skill-name
> /template main
```

## 可用命令

| 命令 | 描述 |
|------|------|
| /template xxx | xxx |

## 配置选项

```json
{
  "option1": "value1"
}
```

## 示例

### 示例 1：xxx

```
> 用户输入
Claude 响应
```

## 贡献指南

欢迎贡献！请阅读 CONTRIBUTING.md

## 许可证

MIT
```

## 15.6 Skills 生态

### 15.6.1 官方 Skills

Anthropic 提供的官方 Skills：

| Skill | 描述 |
|-------|------|
| code-review | 代码审查专家 |
| test-generator | 测试用例生成 |
| documentation | 文档编写助手 |
| refactoring | 代码重构专家 |
| security-audit | 安全审计 |

### 15.6.2 社区 Skills

社区贡献的热门 Skills：

| Skill | 描述 |
|-------|------|
| react-developer | React 开发专家 |
| vue-developer | Vue 开发专家 |
| python-expert | Python 开发专家 |
| devops-helper | DevOps 助手 |
| api-designer | API 设计专家 |

### 15.6.3 发布 Skills

```bash
# 验证 Skill
claude skills validate ./my-skill

# 打包
claude skills pack ./my-skill

# 发布到社区
claude skills publish ./my-skill
```

## 15.7 本章小结

Skills 系统为 Claude Code 提供了强大的能力扩展机制，通过封装领域知识、工具和工作流，实现了能力的模块化和复用。

在下一章中，我们将探讨 Spec 规范驱动开发，学习如何使用规范文档指导开发过程。

---

**关键要点回顾**：

1. Skills 是 Claude Code 的能力扩展机制
2. 一个 Skill 包含提示词、工具、Hooks 和配置
3. 可以通过 skill.json 定义 Skill 元数据
4. 支持安装、激活、管理等操作
5. 遵循最佳实践可以创建高质量的 Skills

**Skill 开发检查清单**：

- [ ] 清晰的角色定义和能力边界
- [ ] 完善的提示词和模板
- [ ] 必要的自定义工具
- [ ] 配套的 Hooks
- [ ] 详细的文档和示例
