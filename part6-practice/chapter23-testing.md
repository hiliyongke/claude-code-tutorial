# 第23章：自动化测试体系搭建

软件测试是保证代码质量的关键环节。一个完善的自动化测试体系能够在开发过程中及早发现问题，降低修复成本，提高交付信心。本章将详细介绍如何使用 Claude Code 辅助搭建完整的自动化测试体系。

## 23.1 测试金字塔与测试策略

### 23.1.1 测试金字塔模型

测试金字塔是由 Mike Cohn 提出的测试策略模型，它建议测试应该按照以下比例分布：

```mermaid
%%{init: {"themeVariables": {"fontSize": "14px"}}}%%
graph TB
    subgraph 测试金字塔
        E2E["E2E 测试<br/>10%"]
        Integration["集成测试<br/>20%"]
        Unit["单元测试<br/>70%"]
    end
    
    E2E --> Integration
    Integration --> Unit
    
    style E2E fill:#ffcdd2
    style Integration fill:#fff9c4
    style Unit fill:#c8e6c9
```

**测试金字塔说明**：
- **顶层（E2E）**：少量端到端测试，验证完整用户流程
- **中层（集成）**：适量集成测试，验证模块间交互
- **底层（单元）**：大量单元测试，验证独立功能单元

各层测试的特点：

| 测试类型 | 执行速度 | 维护成本 | 覆盖范围 | 反馈精度 |
|---------|---------|---------|---------|---------|
| 单元测试 | 快 | 低 | 窄 | 高 |
| 集成测试 | 中 | 中 | 中 | 中 |
| E2E测试 | 慢 | 高 | 广 | 低 |

### 23.1.2 使用 Claude Code 制定测试策略

```bash
claude "请为一个电商系统制定测试策略，包含：
1. 各层测试的覆盖目标
2. 测试优先级排序
3. 测试工具选型
4. 测试环境规划"
```

## 23.2 单元测试

### 23.2.1 单元测试基础

单元测试是对代码最小可测试单元的验证，通常是函数或方法级别。

```bash
claude "请为以下 JavaScript 函数生成完整的单元测试，使用 Jest 框架：

function calculateDiscount(price, customerType, quantity) {
    let discount = 0;
    
    // 会员折扣
    if (customerType === 'vip') {
        discount += 0.1;
    } else if (customerType === 'premium') {
        discount += 0.05;
    }
    
    // 批量折扣
    if (quantity >= 100) {
        discount += 0.15;
    } else if (quantity >= 50) {
        discount += 0.1;
    } else if (quantity >= 10) {
        discount += 0.05;
    }
    
    // 最大折扣限制
    discount = Math.min(discount, 0.3);
    
    return price * (1 - discount);
}

要求覆盖：
1. 正常场景
2. 边界条件
3. 异常输入"
```

生成的测试代码：

```javascript
// __tests__/calculateDiscount.test.js
describe('calculateDiscount', () => {
    describe('会员折扣', () => {
        it('VIP 会员应享受 10% 折扣', () => {
            expect(calculateDiscount(100, 'vip', 1)).toBe(90);
        });

        it('Premium 会员应享受 5% 折扣', () => {
            expect(calculateDiscount(100, 'premium', 1)).toBe(95);
        });

        it('普通会员无折扣', () => {
            expect(calculateDiscount(100, 'regular', 1)).toBe(100);
        });
    });

    describe('批量折扣', () => {
        it('购买 100 件及以上应享受 15% 批量折扣', () => {
            expect(calculateDiscount(100, 'regular', 100)).toBe(85);
        });

        it('购买 50-99 件应享受 10% 批量折扣', () => {
            expect(calculateDiscount(100, 'regular', 50)).toBe(90);
        });

        it('购买 10-49 件应享受 5% 批量折扣', () => {
            expect(calculateDiscount(100, 'regular', 10)).toBe(95);
        });

        it('购买少于 10 件无批量折扣', () => {
            expect(calculateDiscount(100, 'regular', 9)).toBe(100);
        });
    });

    describe('折扣叠加', () => {
        it('VIP + 100件 = 25% 折扣', () => {
            expect(calculateDiscount(100, 'vip', 100)).toBe(75);
        });

        it('Premium + 50件 = 15% 折扣', () => {
            expect(calculateDiscount(100, 'premium', 50)).toBe(85);
        });
    });

    describe('最大折扣限制', () => {
        it('折扣不应超过 30%', () => {
            // VIP(10%) + 100件(15%) = 25%，未超限
            expect(calculateDiscount(100, 'vip', 100)).toBe(75);
        });
    });

    describe('边界条件', () => {
        it('数量边界：9 件无批量折扣', () => {
            expect(calculateDiscount(100, 'regular', 9)).toBe(100);
        });

        it('数量边界：10 件有 5% 批量折扣', () => {
            expect(calculateDiscount(100, 'regular', 10)).toBe(95);
        });

        it('数量边界：49 件有 5% 批量折扣', () => {
            expect(calculateDiscount(100, 'regular', 49)).toBe(95);
        });

        it('数量边界：50 件有 10% 批量折扣', () => {
            expect(calculateDiscount(100, 'regular', 50)).toBe(90);
        });
    });

    describe('异常输入', () => {
        it('价格为 0 应返回 0', () => {
            expect(calculateDiscount(0, 'vip', 100)).toBe(0);
        });

        it('未知会员类型应无会员折扣', () => {
            expect(calculateDiscount(100, 'unknown', 1)).toBe(100);
        });

        it('数量为 0 应无批量折扣', () => {
            expect(calculateDiscount(100, 'regular', 0)).toBe(100);
        });
    });
});
```

### 23.2.2 测试替身（Test Doubles）

```bash
claude "请演示如何使用 Jest 的 Mock 功能测试以下依赖外部服务的代码：

class OrderService {
    constructor(paymentGateway, inventoryService, notificationService) {
        this.paymentGateway = paymentGateway;
        this.inventoryService = inventoryService;
        this.notificationService = notificationService;
    }
    
    async processOrder(order) {
        // 检查库存
        const available = await this.inventoryService.checkStock(order.items);
        if (!available) {
            throw new Error('库存不足');
        }
        
        // 处理支付
        const paymentResult = await this.paymentGateway.charge(order.total);
        if (!paymentResult.success) {
            throw new Error('支付失败');
        }
        
        // 扣减库存
        await this.inventoryService.deductStock(order.items);
        
        // 发送通知
        await this.notificationService.sendOrderConfirmation(order);
        
        return { orderId: order.id, status: 'completed' };
    }
}"
```

Mock 测试示例：

```javascript
// __tests__/OrderService.test.js
describe('OrderService', () => {
    let orderService;
    let mockPaymentGateway;
    let mockInventoryService;
    let mockNotificationService;

    beforeEach(() => {
        // 创建 Mock 对象
        mockPaymentGateway = {
            charge: jest.fn(),
        };
        mockInventoryService = {
            checkStock: jest.fn(),
            deductStock: jest.fn(),
        };
        mockNotificationService = {
            sendOrderConfirmation: jest.fn(),
        };

        orderService = new OrderService(
            mockPaymentGateway,
            mockInventoryService,
            mockNotificationService
        );
    });

    const createTestOrder = () => ({
        id: 'ORD-001',
        items: [{ productId: 'P1', quantity: 2 }],
        total: 100,
    });

    describe('processOrder', () => {
        it('成功处理订单时应返回完成状态', async () => {
            const order = createTestOrder();
            
            mockInventoryService.checkStock.mockResolvedValue(true);
            mockPaymentGateway.charge.mockResolvedValue({ success: true });
            mockInventoryService.deductStock.mockResolvedValue();
            mockNotificationService.sendOrderConfirmation.mockResolvedValue();

            const result = await orderService.processOrder(order);

            expect(result).toEqual({ orderId: 'ORD-001', status: 'completed' });
            expect(mockInventoryService.checkStock).toHaveBeenCalledWith(order.items);
            expect(mockPaymentGateway.charge).toHaveBeenCalledWith(100);
            expect(mockInventoryService.deductStock).toHaveBeenCalledWith(order.items);
            expect(mockNotificationService.sendOrderConfirmation).toHaveBeenCalledWith(order);
        });

        it('库存不足时应抛出错误', async () => {
            const order = createTestOrder();
            mockInventoryService.checkStock.mockResolvedValue(false);

            await expect(orderService.processOrder(order))
                .rejects.toThrow('库存不足');
            
            expect(mockPaymentGateway.charge).not.toHaveBeenCalled();
        });

        it('支付失败时应抛出错误且不扣减库存', async () => {
            const order = createTestOrder();
            mockInventoryService.checkStock.mockResolvedValue(true);
            mockPaymentGateway.charge.mockResolvedValue({ success: false });

            await expect(orderService.processOrder(order))
                .rejects.toThrow('支付失败');
            
            expect(mockInventoryService.deductStock).not.toHaveBeenCalled();
        });
    });
});
```

## 23.3 集成测试

### 23.3.1 API 集成测试

```bash
claude "请为 Express.js REST API 编写集成测试，使用 Supertest：

// routes/users.js
router.post('/users', async (req, res) => {
    const { email, name, password } = req.body;
    const user = await userService.create({ email, name, password });
    res.status(201).json(user);
});

router.get('/users/:id', async (req, res) => {
    const user = await userService.findById(req.params.id);
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
});

要求：
1. 测试成功场景
2. 测试错误场景
3. 使用测试数据库"
```

集成测试代码：

```javascript
// __tests__/integration/users.test.js
const request = require('supertest');
const app = require('../../src/app');
const { prisma } = require('../../src/config/database');

describe('Users API', () => {
    beforeAll(async () => {
        // 连接测试数据库
        await prisma.$connect();
    });

    afterAll(async () => {
        await prisma.$disconnect();
    });

    beforeEach(async () => {
        // 清理测试数据
        await prisma.user.deleteMany();
    });

    describe('POST /api/users', () => {
        it('应成功创建用户并返回 201', async () => {
            const userData = {
                email: 'test@example.com',
                name: 'Test User',
                password: 'SecurePass123!',
            };

            const response = await request(app)
                .post('/api/users')
                .send(userData)
                .expect(201);

            expect(response.body).toMatchObject({
                email: 'test@example.com',
                name: 'Test User',
            });
            expect(response.body.id).toBeDefined();
            expect(response.body.password).toBeUndefined();
        });

        it('邮箱重复时应返回 400', async () => {
            await prisma.user.create({
                data: {
                    email: 'existing@example.com',
                    name: 'Existing User',
                    passwordHash: 'hash',
                },
            });

            const response = await request(app)
                .post('/api/users')
                .send({
                    email: 'existing@example.com',
                    name: 'New User',
                    password: 'SecurePass123!',
                })
                .expect(400);

            expect(response.body.error).toContain('邮箱已被注册');
        });

        it('缺少必填字段时应返回 400', async () => {
            const response = await request(app)
                .post('/api/users')
                .send({ email: 'test@example.com' })
                .expect(400);

            expect(response.body.errors).toBeDefined();
        });
    });

    describe('GET /api/users/:id', () => {
        it('应返回指定用户', async () => {
            const user = await prisma.user.create({
                data: {
                    email: 'test@example.com',
                    name: 'Test User',
                    passwordHash: 'hash',
                },
            });

            const response = await request(app)
                .get(`/api/users/${user.id}`)
                .expect(200);

            expect(response.body).toMatchObject({
                id: user.id,
                email: 'test@example.com',
                name: 'Test User',
            });
        });

        it('用户不存在时应返回 404', async () => {
            const response = await request(app)
                .get('/api/users/nonexistent-id')
                .expect(404);

            expect(response.body.error).toBe('User not found');
        });
    });
});
```

### 23.3.2 数据库集成测试

```bash
claude "请为 Prisma ORM 的 Repository 层编写集成测试：

class TaskRepository {
    async create(data) {
        return prisma.task.create({ data });
    }
    
    async findByProjectId(projectId, options = {}) {
        const { status, page = 1, limit = 20 } = options;
        return prisma.task.findMany({
            where: {
                projectId,
                ...(status && { status }),
            },
            skip: (page - 1) * limit,
            take: limit,
            orderBy: { createdAt: 'desc' },
        });
    }
}"
```

## 23.4 端到端测试

### 23.4.1 使用 Playwright 进行 E2E 测试

```bash
claude "请使用 Playwright 为任务管理系统编写端到端测试，覆盖：
1. 用户登录流程
2. 创建任务流程
3. 任务状态变更流程"
```

E2E 测试代码：

```typescript
// e2e/task-management.spec.ts
import { test, expect } from '@playwright/test';

test.describe('任务管理系统', () => {
    test.beforeEach(async ({ page }) => {
        // 登录
        await page.goto('/login');
        await page.fill('[data-testid="email-input"]', 'test@example.com');
        await page.fill('[data-testid="password-input"]', 'password123');
        await page.click('[data-testid="login-button"]');
        await expect(page).toHaveURL('/dashboard');
    });

    test('用户可以创建新任务', async ({ page }) => {
        // 导航到项目
        await page.click('[data-testid="project-link-1"]');
        
        // 点击创建任务按钮
        await page.click('[data-testid="create-task-button"]');
        
        // 填写任务表单
        await page.fill('[data-testid="task-title-input"]', '测试任务');
        await page.fill('[data-testid="task-description-input"]', '这是一个测试任务');
        await page.selectOption('[data-testid="task-priority-select"]', 'HIGH');
        
        // 提交表单
        await page.click('[data-testid="submit-task-button"]');
        
        // 验证任务创建成功
        await expect(page.locator('[data-testid="task-card"]').filter({ hasText: '测试任务' })).toBeVisible();
    });

    test('用户可以通过拖拽改变任务状态', async ({ page }) => {
        await page.click('[data-testid="project-link-1"]');
        
        // 获取任务卡片和目标列
        const taskCard = page.locator('[data-testid="task-card"]').first();
        const inProgressColumn = page.locator('[data-testid="column-IN_PROGRESS"]');
        
        // 执行拖拽
        await taskCard.dragTo(inProgressColumn);
        
        // 验证任务状态已更新
        await expect(inProgressColumn.locator('[data-testid="task-card"]')).toHaveCount(1);
    });

    test('用户可以筛选任务', async ({ page }) => {
        await page.click('[data-testid="project-link-1"]');
        
        // 选择筛选条件
        await page.selectOption('[data-testid="status-filter"]', 'TODO');
        
        // 验证只显示待办任务
        const taskCards = page.locator('[data-testid="task-card"]');
        await expect(taskCards).toHaveCount(await page.locator('[data-testid="task-card"][data-status="TODO"]').count());
    });
});
```

## 23.5 测试覆盖率与质量指标

### 23.5.1 配置覆盖率报告

```bash
claude "请配置 Jest 的代码覆盖率报告，要求：
1. 设置覆盖率阈值
2. 排除测试文件和配置文件
3. 生成 HTML 报告"
```

Jest 配置：

```javascript
// jest.config.js
module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    roots: ['<rootDir>/src', '<rootDir>/tests'],
    testMatch: ['**/*.test.ts', '**/*.spec.ts'],
    
    // 覆盖率配置
    collectCoverage: true,
    collectCoverageFrom: [
        'src/**/*.{ts,js}',
        '!src/**/*.d.ts',
        '!src/**/index.ts',
        '!src/config/**',
        '!src/types/**',
    ],
    coverageDirectory: 'coverage',
    coverageReporters: ['text', 'lcov', 'html'],
    
    // 覆盖率阈值
    coverageThreshold: {
        global: {
            branches: 80,
            functions: 80,
            lines: 80,
            statements: 80,
        },
        './src/services/': {
            branches: 90,
            functions: 90,
            lines: 90,
            statements: 90,
        },
    },
};
```

### 23.5.2 持续集成中的测试

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:unit
      
      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
      
      - name: Upload coverage report
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

## 23.6 本章小结

本章详细介绍了如何使用 Claude Code 搭建完整的自动化测试体系：

1. **测试策略**：理解测试金字塔，合理分配测试资源
2. **单元测试**：编写高质量的单元测试，使用 Mock 隔离依赖
3. **集成测试**：验证组件间的协作，测试真实的数据库交互
4. **E2E 测试**：模拟用户行为，验证完整业务流程
5. **质量指标**：配置覆盖率报告，设置质量门禁

Claude Code 在测试中的应用：
- 根据代码自动生成测试用例
- 识别边界条件和异常场景
- 生成 Mock 对象和测试数据
- 分析测试覆盖率缺口
