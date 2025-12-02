# 第6章：CLAUDE.md 配置详解（Memory 系统）

## 6.1 CLAUDE.md 与 Memory 系统概述

CLAUDE.md 是 Claude Code 的核心配置机制，也是其 **Memory（记忆）系统** 的载体。它允许 Claude 记住您的偏好、项目规范和工作流程，并在后续会话中自动应用这些信息。

### 6.1.1 设计理念

CLAUDE.md 的设计体现了以下原则：

**人机可读**：采用 Markdown 格式，既可以被 Claude 解析理解，也方便开发者阅读和维护。

**版本可控**：作为项目文件的一部分，可以纳入版本控制，团队成员共享相同的配置。

**层级覆盖**：支持企业、用户、项目多个层级的配置，下层配置可覆盖上层。

**渐进增强**：从简单的项目描述到复杂的行为规则，可根据需求逐步完善。

### 6.1.2 Memory 层级结构

Claude Code 采用分层级的记忆系统：

| 记忆类型 | 存储位置 | 用途 | 适用场景 |
|---------|---------|------|---------|
| **企业策略** | `/Library/Application Support/ClaudeCode/`（macOS） | 全组织范围的指令，由 IT/DevOps 管理 | 公司编码标准、安全策略、合规要求 |
| **用户记忆** | `~/.claude/CLAUDE.md` | 个人对所有项目的偏好设置 | 个人代码风格偏好、常用工具快捷键 |
| **项目记忆** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队共享的项目指令 | 项目架构、代码规范、常用工作流 |

**关键点**：更高层级的记忆文件会先被加载，低层级的记忆可以覆盖或补充高层级的指令。

### 6.1.3 加载机制

Claude Code 会自动从当前工作目录开始，**向上递归**查找直到根目录，加载所有找到的 `CLAUDE.md` 文件。

例如，在 `/project/team-a/src` 目录下工作时，Claude 会加载：
1. `/project/team-a/src/CLAUDE.md`（如果存在）
2. `/project/team-a/CLAUDE.md`（如果存在）
3. `/project/CLAUDE.md`（如果存在）

此外，它还会发现并**在需要时**加载当前目录子树下的 `CLAUDE.md` 文件。

```
┌─────────────────────────────────────────────────────────┐
│                    配置加载流程                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 加载企业策略配置                                     │
│         ↓                                               │
│  2. 加载用户配置 (~/.claude/CLAUDE.md)                  │
│         ↓                                               │
│  3. 递归加载项目配置（从根目录到当前目录）                │
│         ↓                                               │
│  4. 发现子目录配置（按需加载）                           │
│         ↓                                               │
│  6. 最终配置生效                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 6.1.4 Memory 快捷操作

Claude Code 提供了便捷的 Memory 管理方式：

**快速添加记忆（`#` 快捷键）**

在对话中输入以 `#` 开头的内容，可以快速创建一条记忆：

```
# 代码注释必须使用中文
# 使用 const 和 let，避免使用 var
# 优先使用 async/await 而非 Promise.then
```

系统会提示您选择将这条记忆保存到哪个记忆文件中（用户记忆或项目记忆）。

**编辑记忆（`/memory` 命令）**

在会话中使用 `/memory` 命令，会在默认编辑器中打开所有已加载的记忆文件：

```bash
> /memory
# 打开编辑器，显示所有 CLAUDE.md 文件
```

**初始化项目记忆（`/init` 命令）**

在项目根目录下使用 `/init` 命令，可以快速生成一个基础的 `CLAUDE.md` 文件模板：

```bash
> /init
# 引导生成项目配置文件
```

### 6.1.5 导入其他文件（`@` 语法）

可以在 `CLAUDE.md` 文件中使用 `@文件路径` 的语法来导入其他文件的内容：

```markdown
# 项目说明
请参考 @README.md 了解项目概况。
构建和测试命令详见 @package.json。

# 团队工作流
- Git 提交规范 @docs/git_guide.md
- 个人配置可参考 @~/.claude/my_prefs.md（此文件不会提交到代码库）
```

## 6.2 CLAUDE.md 基础结构

### 6.2.1 最小配置示例

一个最基础的 CLAUDE.md 文件只需要包含项目描述：

```markdown
# Project: My Web Application

这是一个基于 React 和 Node.js 的全栈 Web 应用。

## 技术栈
- 前端：React 18, TypeScript, Tailwind CSS
- 后端：Node.js, Express, PostgreSQL
- 部署：Docker, AWS
```

即使是这样简单的描述，也能帮助 Claude 更好地理解项目上下文。

### 6.2.2 完整配置结构

一个完整的 CLAUDE.md 文件通常包含以下部分：

```markdown
# Project: [项目名称]

[项目简介]

## 技术栈

[技术栈描述]

## 项目结构

[目录结构说明]

## 开发规范

[编码规范和约定]

## 常用命令

[开发、测试、部署命令]

## 注意事项

[特殊说明和警告]

## Claude 指令

[对 Claude 行为的具体指令]
```

### 6.2.3 配置解析规则

Claude 会按照以下规则解析 CLAUDE.md：

1. **标题层级**：一级标题（#）标识主要部分，二级标题（##）标识子部分
2. **代码块**：被识别为代码示例或命令
3. **列表**：被识别为枚举项或步骤
4. **强调文本**：加粗（**）或斜体（*）的文本会被特别关注

## 6.3 项目信息配置

### 6.3.1 项目描述

清晰的项目描述帮助 Claude 理解项目背景：

```markdown
# Project: E-Commerce Platform

这是一个面向中小企业的电子商务平台，提供商品管理、订单处理、
支付集成和物流跟踪等核心功能。

## 业务背景

- 目标用户：中小型零售商
- 日均订单量：约 5000 单
- 主要市场：中国大陆地区

## 核心功能模块

1. **商品管理**：商品 CRUD、分类管理、库存管理
2. **订单系统**：订单创建、状态流转、退款处理
3. **支付集成**：支付宝、微信支付、银联
4. **用户系统**：注册登录、权限管理、会员体系
```

### 6.3.2 技术栈声明

明确的技术栈声明使 Claude 生成的代码更符合项目实际：

```markdown
## 技术栈

### 前端
- **框架**：React 18.2 with TypeScript 5.0
- **状态管理**：Zustand 4.x
- **UI 组件**：Ant Design 5.x
- **样式方案**：CSS Modules + Tailwind CSS
- **构建工具**：Vite 5.x

### 后端
- **运行时**：Node.js 20 LTS
- **框架**：NestJS 10.x
- **ORM**：Prisma 5.x
- **数据库**：PostgreSQL 15
- **缓存**：Redis 7.x

### 基础设施
- **容器化**：Docker + Docker Compose
- **CI/CD**：GitHub Actions
- **部署**：AWS ECS + RDS
- **监控**：Prometheus + Grafana
```

### 6.3.3 项目结构说明

详细的目录结构说明帮助 Claude 快速定位文件：

```markdown
## 项目结构

```
├── apps/
│   ├── web/                 # 前端应用
│   │   ├── src/
│   │   │   ├── components/  # 通用组件
│   │   │   ├── pages/       # 页面组件
│   │   │   ├── hooks/       # 自定义 Hooks
│   │   │   ├── stores/      # Zustand stores
│   │   │   ├── services/    # API 调用服务
│   │   │   └── utils/       # 工具函数
│   │   └── package.json
│   │
│   └── api/                 # 后端应用
│       ├── src/
│       │   ├── modules/     # 功能模块
│       │   ├── common/      # 公共代码
│       │   ├── config/      # 配置文件
│       │   └── main.ts      # 入口文件
│       └── package.json
│
├── packages/
│   └── shared/              # 共享代码包
│       ├── types/           # 类型定义
│       └── utils/           # 共享工具
│
├── docker/                  # Docker 配置
├── docs/                    # 项目文档
└── package.json             # 根配置（monorepo）
```

### 关键目录说明

- `apps/web/src/components/`：存放可复用的 UI 组件
- `apps/api/src/modules/`：每个模块包含 controller、service、dto
- `packages/shared/types/`：前后端共享的 TypeScript 类型
```

## 6.4 开发规范配置

### 6.4.1 编码规范

定义编码规范确保 Claude 生成的代码风格一致：

```markdown
## 编码规范

### 命名约定

- **文件命名**：
  - React 组件：PascalCase（如 `UserProfile.tsx`）
  - 工具函数：camelCase（如 `formatDate.ts`）
  - 常量文件：SCREAMING_SNAKE_CASE（如 `API_ENDPOINTS.ts`）

- **变量命名**：
  - 普通变量：camelCase
  - 常量：UPPER_SNAKE_CASE
  - 私有属性：_camelCase
  - 布尔值：is/has/can 前缀（如 `isLoading`）

- **函数命名**：
  - 事件处理：handle 前缀（如 `handleSubmit`）
  - 获取数据：get/fetch 前缀（如 `fetchUserList`）
  - 设置数据：set/update 前缀（如 `setUserName`）

### 代码风格

- 使用 2 空格缩进
- 字符串使用单引号
- 语句末尾不加分号（前端）/ 加分号（后端）
- 最大行宽 100 字符
- 文件末尾保留空行

### 注释规范

- 公共 API 必须有 JSDoc/TSDoc 注释
- 复杂逻辑需要行内注释说明
- TODO 注释格式：`// TODO(author): description`
- 禁止提交被注释的代码块
```

### 6.4.2 架构规范

定义架构规范指导 Claude 的设计决策：

```markdown
### 架构规范

#### 前端架构

1. **组件设计原则**
   - 遵循单一职责原则
   - 优先使用函数组件和 Hooks
   - 容器组件与展示组件分离
   - 组件 props 必须定义 TypeScript 接口

2. **状态管理原则**
   - 局部状态使用 useState
   - 跨组件状态使用 Zustand store
   - 服务端状态使用 React Query
   - 避免 prop drilling，超过 2 层使用 Context 或 Store

3. **目录组织原则**
   - 按功能模块组织，非按文件类型
   - 相关文件就近放置
   - index.ts 只用于导出，不包含逻辑

#### 后端架构

1. **模块设计原则**
   - 每个模块独立，通过依赖注入通信
   - Controller 只处理 HTTP 相关逻辑
   - Service 包含业务逻辑
   - Repository 模式访问数据库

2. **API 设计原则**
   - RESTful 风格
   - 统一响应格式：`{ code, message, data }`
   - 分页格式：`{ items, total, page, pageSize }`
   - 错误码体系：业务错误 4xxxx，系统错误 5xxxx

3. **数据库原则**
   - 使用 Prisma 进行数据库操作
   - 所有表必须有 createdAt、updatedAt 字段
   - 软删除使用 deletedAt 字段
   - 关联查询注意 N+1 问题
```

### 6.4.3 Git 规范

定义 Git 工作流规范：

```markdown
### Git 规范

#### 分支命名

- 主分支：`main`
- 开发分支：`develop`
- 功能分支：`feature/[issue-id]-brief-description`
- 修复分支：`fix/[issue-id]-brief-description`
- 发布分支：`release/v[version]`

#### Commit 消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型**：
- `feat`：新功能
- `fix`：Bug 修复
- `docs`：文档更新
- `style`：代码格式（不影响功能）
- `refactor`：重构
- `test`：测试相关
- `chore`：构建/工具相关

**示例**：
```
feat(order): add order export functionality

- Support CSV and Excel export formats
- Add date range filter for export
- Implement background job for large exports

Closes #123
```
```

## 6.5 Claude 行为指令

### 6.5.1 通用指令

通过指令控制 Claude 的行为模式：

```markdown
## Claude 指令

### 通用行为

- 生成代码时，始终遵循本项目的编码规范
- 修改文件前，先阅读相关文件了解现有实现
- 创建新文件时，参考同目录下现有文件的风格
- 不确定时，询问而非假设

### 代码生成

- 生成 TypeScript 代码时，提供完整的类型定义
- 生成组件时，包含必要的 props 接口定义
- 生成 API 接口时，包含请求和响应的类型定义
- 添加适当的错误处理和边界情况处理

### 文件操作

- 修改配置文件时格外谨慎，先确认影响范围
- 不要修改 lock 文件（package-lock.json, yarn.lock）
- 不要修改 .env 文件中的敏感信息
- 创建新模块时，同时更新相关的 index.ts 导出
```

### 6.5.2 禁止事项

明确列出禁止的操作：

```markdown
### 禁止事项

**绝对禁止**：
- 删除或修改 `.env*` 文件中的密钥和敏感配置
- 直接修改 `node_modules` 目录下的文件
- 修改 `migrations` 目录下已执行的迁移文件
- 在代码中硬编码密码、密钥等敏感信息

**除非明确要求，否则不要**：
- 升级 package.json 中的依赖版本
- 修改 ESLint、Prettier 等工具配置
- 修改 CI/CD 配置文件
- 修改 Docker 配置文件
```

### 6.5.3 偏好设置

设置 Claude 的偏好行为：

```markdown
### 偏好设置

**代码风格偏好**：
- 优先使用 `async/await` 而非 `.then()` 链
- 优先使用 `const`，必要时使用 `let`，避免 `var`
- 优先使用箭头函数，类方法除外
- 优先使用模板字符串而非字符串拼接
- 优先使用解构赋值

**库选择偏好**：
- HTTP 请求：使用项目中已有的 axios 实例
- 日期处理：使用 dayjs
- 工具函数：优先使用项目 utils，其次 lodash-es
- 表单验证：使用 zod

**测试偏好**：
- 单元测试使用 Jest + React Testing Library
- E2E 测试使用 Playwright
- 测试文件与源文件同目录，命名为 `*.test.ts(x)`
```

## 6.6 常用命令配置

### 6.6.1 开发命令

记录常用命令供 Claude 参考和执行：

```markdown
## 常用命令

### 开发环境

```bash
# 安装依赖
pnpm install

# 启动开发服务器（前端 + 后端）
pnpm dev

# 只启动前端
pnpm dev:web

# 只启动后端
pnpm dev:api

# 启动数据库（Docker）
docker-compose up -d postgres redis
```

### 测试命令

```bash
# 运行所有测试
pnpm test

# 运行单元测试
pnpm test:unit

# 运行 E2E 测试
pnpm test:e2e

# 测试覆盖率报告
pnpm test:coverage

# 监听模式运行测试
pnpm test:watch
```

### 构建部署

```bash
# 构建生产版本
pnpm build

# 本地预览生产构建
pnpm preview

# 数据库迁移
pnpm db:migrate

# 生成 Prisma 客户端
pnpm db:generate
```

### 代码质量

```bash
# 代码格式化
pnpm format

# 代码检查
pnpm lint

# 类型检查
pnpm typecheck
```
```

## 6.7 高级配置技巧

### 6.7.1 条件配置

可以为不同场景提供条件性指导：

```markdown
## 场景特定指令

### 当处理用户认证相关代码时

- 所有密码必须使用 bcrypt 加密，rounds >= 10
- JWT token 过期时间：access token 15分钟，refresh token 7天
- 敏感操作需要二次验证
- 登录失败需要记录日志并实现防暴力破解

### 当处理支付相关代码时

- 所有金额使用整数（分）存储和计算，避免浮点数精度问题
- 支付回调必须验证签名
- 关键操作必须有事务保护
- 必须记录完整的支付日志

### 当处理文件上传时

- 验证文件类型和大小
- 生成唯一文件名，避免覆盖
- 图片需要生成缩略图
- 使用 OSS 存储，不存储在本地
```

### 6.7.2 模板配置

提供代码模板供 Claude 参考：

```markdown
## 代码模板

### React 组件模板

```tsx
import { FC, memo } from 'react';
import styles from './ComponentName.module.css';

interface ComponentNameProps {
  // props definition
}

export const ComponentName: FC<ComponentNameProps> = memo(({ ...props }) => {
  return (
    <div className={styles.container}>
      {/* component content */}
    </div>
  );
});

ComponentName.displayName = 'ComponentName';
```

### NestJS Controller 模板

```typescript
import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { ModuleService } from './module.service';
import { CreateDto, QueryDto } from './dto';

@ApiTags('Module')
@Controller('module')
export class ModuleController {
  constructor(private readonly service: ModuleService) {}

  @Get()
  @ApiOperation({ summary: 'Get list' })
  async findAll(@Query() query: QueryDto) {
    return this.service.findAll(query);
  }

  @Post()
  @ApiOperation({ summary: 'Create item' })
  async create(@Body() dto: CreateDto) {
    return this.service.create(dto);
  }
}
```
```

### 6.7.3 外部文档引用

可以引用外部文档：

```markdown
## 参考文档

- [API 文档](./docs/api.md)
- [数据库设计](./docs/database.md)
- [部署指南](./docs/deployment.md)

当需要了解 API 接口详情时，请参考 `docs/api.md`。
当需要了解数据表结构时，请参考 `docs/database.md`。
```

## 6.8 配置最佳实践

### 6.8.1 配置文件组织

对于大型项目，可以将配置拆分：

```
project/
├── CLAUDE.md              # 主配置文件
├── .claude/
│   ├── coding-standards.md  # 编码规范
│   ├── architecture.md      # 架构说明
│   └── commands.md          # 常用命令
```

主配置文件引用其他文件：

```markdown
# Project: Large Enterprise App

## 配置引用

详细配置请参考：
- 编码规范：`.claude/coding-standards.md`
- 架构说明：`.claude/architecture.md`
- 常用命令：`.claude/commands.md`
```

### 6.8.2 团队协作

团队使用 CLAUDE.md 的建议：

1. **纳入版本控制**：CLAUDE.md 应该提交到 Git 仓库
2. **定期更新**：随项目演进更新配置
3. **团队评审**：重要配置变更需要团队评审
4. **文档同步**：保持 CLAUDE.md 与项目文档一致

### 6.8.3 渐进式完善

不必一次性编写完整配置，可以渐进式完善：

**第一阶段**：基础项目信息
```markdown
# Project: My App
基于 React + Node.js 的 Web 应用。
```

**第二阶段**：添加技术栈和结构
```markdown
## 技术栈
- React 18, TypeScript
- Node.js, Express

## 项目结构
- src/：源代码
- tests/：测试文件
```

**第三阶段**：添加规范和指令
```markdown
## 编码规范
[详细规范]

## Claude 指令
[行为指令]
```

## 6.9 本章小结

CLAUDE.md 是 Claude Code 的核心配置机制，通过合理配置可以显著提升 Claude 的响应质量和代码生成的准确性。本章详细介绍了 CLAUDE.md 的结构、配置项和最佳实践。

在下一章中，我们将探讨 Claude Code 的权限与安全模型，了解如何安全地使用 Claude Code。

---

**关键要点回顾**：

1. CLAUDE.md 采用 Markdown 格式，人机可读
2. 支持全局、用户、项目多层级配置
3. 核心配置包括：项目信息、技术栈、开发规范、Claude 指令
4. 可以通过指令控制 Claude 的行为偏好和禁止事项
5. 建议渐进式完善配置，并纳入版本控制
