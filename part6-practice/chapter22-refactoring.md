# 第22章：遗留代码重构实战

遗留代码（Legacy Code）是软件开发中不可避免的挑战。无论是接手他人的项目，还是维护自己多年前编写的代码，都需要面对代码质量参差不齐、文档缺失、测试不足等问题。本章将通过实际案例，展示如何使用 Claude Code 系统性地进行遗留代码重构。

## 22.1 遗留代码的识别与评估

### 22.1.1 什么是遗留代码

遗留代码通常具有以下特征：

- 缺乏测试覆盖
- 文档不完整或过时
- 使用过时的技术或模式
- 代码结构混乱，难以理解
- 存在大量技术债务
- 原开发者已离开团队

Michael Feathers 在《修改代码的艺术》中给出了一个简洁的定义：**没有测试的代码就是遗留代码**。

### 22.1.2 使用 Claude Code 评估代码质量

首先，让 Claude Code 对遗留代码进行全面评估：

```bash
claude "请对 src/legacy/ 目录下的代码进行全面评估，输出：
1. 代码规模统计（文件数、代码行数、函数数量）
2. 代码质量问题清单（按严重程度分类）
3. 技术债务评估
4. 重构优先级建议
5. 预估工作量"
```

评估报告示例：

```
## 遗留代码评估报告

### 1. 代码规模统计

| 指标 | 数值 |
|------|------|
| 文件总数 | 47 |
| 代码行数 | 12,350 |
| 函数/方法数 | 423 |
| 类数量 | 28 |
| 平均函数长度 | 29 行 |
| 最大函数长度 | 387 行 |

### 2. 代码质量问题清单

**严重问题（必须修复）**
- [ ] SQL 注入风险：UserRepository.java:145, OrderService.java:89
- [ ] 硬编码密码：config/database.js:12
- [ ] 未处理的异常：PaymentProcessor.java 多处
- [ ] 内存泄漏风险：CacheManager.java:234

**一般问题（建议修复）**
- [ ] 重复代码：OrderValidator 和 ProductValidator 有 60% 相似度
- [ ] 过长函数：OrderProcessor.processOrder() 387 行
- [ ] 过大类：UserService.java 1,200 行，承担过多职责
- [ ] 魔法数字：多处硬编码的数值常量

**轻微问题（可选修复）**
- [ ] 命名不规范：部分变量使用单字母命名
- [ ] 注释过时：多处注释与代码不符
- [ ] 未使用的代码：约 15% 的代码从未被调用

### 3. 技术债务评估

| 类别 | 债务级别 | 说明 |
|------|---------|------|
| 安全债务 | 高 | 存在 SQL 注入、密码泄露风险 |
| 架构债务 | 高 | 缺乏分层，业务逻辑与数据访问混杂 |
| 测试债务 | 高 | 测试覆盖率 < 10% |
| 文档债务 | 中 | 核心模块缺乏文档 |
| 依赖债务 | 中 | 多个依赖版本过旧 |

### 4. 重构优先级建议

1. **P0 - 立即处理**：安全漏洞修复
2. **P1 - 短期计划**：添加核心模块测试、拆分大类
3. **P2 - 中期计划**：架构重构、消除重复代码
4. **P3 - 长期计划**：依赖升级、代码规范统一

### 5. 预估工作量

| 阶段 | 工作量 | 说明 |
|------|--------|------|
| 安全修复 | 2-3 天 | 紧急处理安全问题 |
| 测试补充 | 1-2 周 | 为核心模块添加测试 |
| 核心重构 | 2-3 周 | 拆分大类、消除重复 |
| 架构优化 | 3-4 周 | 分层重构、依赖注入 |
| 总计 | 6-10 周 | 根据团队规模调整 |
```

### 22.1.3 建立重构安全网

在开始重构之前，必须建立测试安全网：

```bash
claude "请为 OrderProcessor.java 这个核心类生成特征测试（Characterization Tests），
目的是捕获当前行为，而非验证正确性。
要求：
1. 覆盖所有公共方法
2. 包含边界条件
3. 记录当前的输出行为"
```

特征测试示例：

```java
// tests/OrderProcessorCharacterizationTest.java
public class OrderProcessorCharacterizationTest {
    
    private OrderProcessor processor;
    
    @BeforeEach
    void setUp() {
        processor = new OrderProcessor();
    }
    
    @Test
    @DisplayName("记录 processOrder 的当前行为 - 正常订单")
    void characterize_processOrder_normalOrder() {
        Order order = createTestOrder("ORD-001", 100.0, "PENDING");
        
        OrderResult result = processor.processOrder(order);
        
        // 记录当前行为，不判断对错
        assertThat(result.getStatus()).isEqualTo("PROCESSED");
        assertThat(result.getTotalAmount()).isEqualTo(108.0); // 含税
        assertThat(result.getProcessedAt()).isNotNull();
    }
    
    @Test
    @DisplayName("记录 processOrder 的当前行为 - 空订单")
    void characterize_processOrder_emptyOrder() {
        Order order = createTestOrder("ORD-002", 0.0, "PENDING");
        
        // 记录当前行为：空订单抛出异常
        assertThatThrownBy(() -> processor.processOrder(order))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessage("Order amount cannot be zero");
    }
    
    @Test
    @DisplayName("记录 processOrder 的当前行为 - 大额订单")
    void characterize_processOrder_largeOrder() {
        Order order = createTestOrder("ORD-003", 10000.0, "PENDING");
        
        OrderResult result = processor.processOrder(order);
        
        // 记录当前行为：大额订单有折扣
        assertThat(result.getDiscount()).isEqualTo(500.0);
        assertThat(result.getTotalAmount()).isEqualTo(10260.0);
    }
    
    // ... 更多特征测试
}
```

## 22.2 安全问题修复

### 22.2.1 SQL 注入修复

```bash
claude "请修复 UserRepository.java 中的 SQL 注入漏洞，
当前代码：
public User findByUsername(String username) {
    String sql = \"SELECT * FROM users WHERE username = '\" + username + \"'\";
    return jdbcTemplate.queryForObject(sql, new UserRowMapper());
}

要求：
1. 使用参数化查询
2. 保持原有功能
3. 添加输入验证"
```

修复后的代码：

```java
// 修复后的 UserRepository.java
public class UserRepository {
    
    private static final String FIND_BY_USERNAME_SQL = 
        "SELECT * FROM users WHERE username = ?";
    
    private static final Pattern USERNAME_PATTERN = 
        Pattern.compile("^[a-zA-Z0-9_]{3,50}$");
    
    public User findByUsername(String username) {
        // 输入验证
        if (username == null || username.isBlank()) {
            throw new IllegalArgumentException("用户名不能为空");
        }
        
        if (!USERNAME_PATTERN.matcher(username).matches()) {
            throw new IllegalArgumentException("用户名格式不正确");
        }
        
        // 使用参数化查询
        return jdbcTemplate.queryForObject(
            FIND_BY_USERNAME_SQL,
            new Object[]{username},
            new UserRowMapper()
        );
    }
}
```

### 22.2.2 敏感信息处理

```bash
claude "请修复 config/database.js 中的硬编码密码问题，
当前代码：
module.exports = {
    host: 'localhost',
    port: 5432,
    database: 'myapp',
    username: 'admin',
    password: 'admin123'  // 硬编码密码
};

要求：
1. 使用环境变量
2. 提供默认值用于开发环境
3. 添加配置验证"
```

修复后的代码：

```javascript
// config/database.js
const Joi = require('joi');

// 配置验证 Schema
const configSchema = Joi.object({
    host: Joi.string().hostname().required(),
    port: Joi.number().port().default(5432),
    database: Joi.string().required(),
    username: Joi.string().required(),
    password: Joi.string().required(),
    ssl: Joi.boolean().default(false),
    poolSize: Joi.number().min(1).max(100).default(10),
});

// 从环境变量读取配置
const rawConfig = {
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT, 10) || 5432,
    database: process.env.DB_NAME,
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    ssl: process.env.DB_SSL === 'true',
    poolSize: parseInt(process.env.DB_POOL_SIZE, 10) || 10,
};

// 验证配置
const { error, value: config } = configSchema.validate(rawConfig, {
    abortEarly: false,
});

if (error) {
    const missingVars = error.details.map(d => d.path.join('.')).join(', ');
    throw new Error(`数据库配置错误，请检查环境变量: ${missingVars}`);
}

module.exports = config;
```

## 22.3 代码结构重构

### 22.3.1 拆分过大的类

```bash
claude "请将 UserService.java（1200行）拆分为多个职责单一的类，
当前类包含以下功能：
1. 用户 CRUD
2. 密码管理
3. 权限验证
4. 邮件通知
5. 日志记录
6. 缓存管理

请提供：
1. 拆分方案
2. 新类的职责定义
3. 重构步骤
4. 迁移后的代码结构"
```

拆分方案：

```
重构前：
UserService.java (1200 行)
├── createUser()
├── updateUser()
├── deleteUser()
├── findUser()
├── changePassword()
├── resetPassword()
├── validatePassword()
├── checkPermission()
├── hasRole()
├── sendWelcomeEmail()
├── sendPasswordResetEmail()
├── logUserAction()
├── cacheUser()
├── invalidateCache()
└── ... (更多方法)

重构后：
├── UserService.java (核心 CRUD，约 150 行)
│   ├── createUser()
│   ├── updateUser()
│   ├── deleteUser()
│   └── findUser()
│
├── PasswordService.java (密码管理，约 100 行)
│   ├── changePassword()
│   ├── resetPassword()
│   └── validatePassword()
│
├── AuthorizationService.java (权限验证，约 120 行)
│   ├── checkPermission()
│   ├── hasRole()
│   └── validateAccess()
│
├── UserNotificationService.java (通知，约 80 行)
│   ├── sendWelcomeEmail()
│   ├── sendPasswordResetEmail()
│   └── sendNotification()
│
├── UserCacheService.java (缓存，约 60 行)
│   ├── cacheUser()
│   ├── getFromCache()
│   └── invalidateCache()
│
└── UserActivityLogger.java (日志，约 50 行)
    ├── logUserAction()
    └── logSecurityEvent()
```

重构后的核心代码：

```java
// UserService.java - 重构后
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserRepository userRepository;
    private final PasswordService passwordService;
    private final UserNotificationService notificationService;
    private final UserCacheService cacheService;
    private final UserActivityLogger activityLogger;
    
    @Transactional
    public User createUser(CreateUserRequest request) {
        // 验证邮箱唯一性
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateEmailException(request.getEmail());
        }
        
        // 创建用户
        User user = User.builder()
            .email(request.getEmail())
            .name(request.getName())
            .passwordHash(passwordService.hashPassword(request.getPassword()))
            .role(UserRole.MEMBER)
            .build();
        
        user = userRepository.save(user);
        
        // 后续处理
        cacheService.cacheUser(user);
        notificationService.sendWelcomeEmail(user);
        activityLogger.logUserAction(user.getId(), "USER_CREATED");
        
        return user;
    }
    
    public User findById(String id) {
        // 先查缓存
        return cacheService.getFromCache(id)
            .orElseGet(() -> {
                User user = userRepository.findById(id)
                    .orElseThrow(() -> new UserNotFoundException(id));
                cacheService.cacheUser(user);
                return user;
            });
    }
    
    @Transactional
    public User updateUser(String id, UpdateUserRequest request) {
        User user = findById(id);
        
        if (request.getName() != null) {
            user.setName(request.getName());
        }
        if (request.getEmail() != null) {
            user.setEmail(request.getEmail());
        }
        
        user = userRepository.save(user);
        cacheService.invalidateCache(id);
        activityLogger.logUserAction(id, "USER_UPDATED");
        
        return user;
    }
    
    @Transactional
    public void deleteUser(String id) {
        User user = findById(id);
        userRepository.delete(user);
        cacheService.invalidateCache(id);
        activityLogger.logUserAction(id, "USER_DELETED");
    }
}
```

### 22.3.2 消除重复代码

```bash
claude "请分析 OrderValidator.java 和 ProductValidator.java 的重复代码，
并提取公共逻辑到基类或工具类：

OrderValidator.java:
public class OrderValidator {
    public ValidationResult validate(Order order) {
        List<String> errors = new ArrayList<>();
        
        if (order.getId() == null || order.getId().isEmpty()) {
            errors.add(\"订单ID不能为空\");
        }
        if (order.getAmount() == null || order.getAmount() <= 0) {
            errors.add(\"订单金额必须大于0\");
        }
        if (order.getCustomerId() == null) {
            errors.add(\"客户ID不能为空\");
        }
        // ... 更多验证
        
        return new ValidationResult(errors.isEmpty(), errors);
    }
}

ProductValidator.java:
public class ProductValidator {
    public ValidationResult validate(Product product) {
        List<String> errors = new ArrayList<>();
        
        if (product.getId() == null || product.getId().isEmpty()) {
            errors.add(\"产品ID不能为空\");
        }
        if (product.getPrice() == null || product.getPrice() <= 0) {
            errors.add(\"产品价格必须大于0\");
        }
        if (product.getName() == null || product.getName().isEmpty()) {
            errors.add(\"产品名称不能为空\");
        }
        // ... 更多验证
        
        return new ValidationResult(errors.isEmpty(), errors);
    }
}"
```

重构后的代码：

```java
// 通用验证框架
public abstract class BaseValidator<T> {
    
    protected final List<ValidationRule<T>> rules = new ArrayList<>();
    
    public ValidationResult validate(T entity) {
        List<String> errors = rules.stream()
            .map(rule -> rule.validate(entity))
            .filter(Optional::isPresent)
            .map(Optional::get)
            .collect(Collectors.toList());
        
        return new ValidationResult(errors.isEmpty(), errors);
    }
    
    protected void addRule(Predicate<T> condition, String errorMessage) {
        rules.add(entity -> condition.test(entity) 
            ? Optional.empty() 
            : Optional.of(errorMessage));
    }
    
    protected void addNotNullRule(Function<T, Object> getter, String fieldName) {
        addRule(
            entity -> getter.apply(entity) != null,
            fieldName + "不能为空"
        );
    }
    
    protected void addNotEmptyRule(Function<T, String> getter, String fieldName) {
        addRule(
            entity -> {
                String value = getter.apply(entity);
                return value != null && !value.isEmpty();
            },
            fieldName + "不能为空"
        );
    }
    
    protected void addPositiveNumberRule(Function<T, Number> getter, String fieldName) {
        addRule(
            entity -> {
                Number value = getter.apply(entity);
                return value != null && value.doubleValue() > 0;
            },
            fieldName + "必须大于0"
        );
    }
}

// 订单验证器
public class OrderValidator extends BaseValidator<Order> {
    
    public OrderValidator() {
        addNotEmptyRule(Order::getId, "订单ID");
        addPositiveNumberRule(Order::getAmount, "订单金额");
        addNotNullRule(Order::getCustomerId, "客户ID");
        addNotNullRule(Order::getOrderDate, "订单日期");
        
        // 自定义规则
        addRule(
            order -> order.getItems() != null && !order.getItems().isEmpty(),
            "订单必须包含至少一个商品"
        );
    }
}

// 产品验证器
public class ProductValidator extends BaseValidator<Product> {
    
    public ProductValidator() {
        addNotEmptyRule(Product::getId, "产品ID");
        addNotEmptyRule(Product::getName, "产品名称");
        addPositiveNumberRule(Product::getPrice, "产品价格");
        
        // 自定义规则
        addRule(
            product -> product.getStock() >= 0,
            "库存不能为负数"
        );
    }
}
```

### 22.3.3 重构过长函数

```bash
claude "请将以下 387 行的 processOrder 方法重构为多个小函数，
每个函数职责单一，便于测试和维护：

public OrderResult processOrder(Order order) {
    // 第1-50行：订单验证
    // 第51-120行：库存检查
    // 第121-200行：价格计算
    // 第201-280行：支付处理
    // 第281-350行：物流安排
    // 第351-387行：通知发送
    ...
}

请提供重构后的代码结构和关键实现"
```

重构后的代码：

```java
// OrderProcessor.java - 重构后
@Service
@RequiredArgsConstructor
public class OrderProcessor {
    
    private final OrderValidator orderValidator;
    private final InventoryService inventoryService;
    private final PricingService pricingService;
    private final PaymentService paymentService;
    private final ShippingService shippingService;
    private final NotificationService notificationService;
    
    @Transactional
    public OrderResult processOrder(Order order) {
        // 1. 验证订单
        ValidationResult validation = orderValidator.validate(order);
        if (!validation.isValid()) {
            return OrderResult.failed(validation.getErrors());
        }
        
        // 2. 检查并预留库存
        InventoryReservation reservation = reserveInventory(order);
        
        try {
            // 3. 计算价格
            PriceBreakdown pricing = calculatePricing(order);
            
            // 4. 处理支付
            PaymentResult payment = processPayment(order, pricing);
            
            // 5. 安排物流
            ShippingInfo shipping = arrangeShipping(order);
            
            // 6. 发送通知
            sendNotifications(order, payment, shipping);
            
            // 7. 构建结果
            return buildSuccessResult(order, pricing, payment, shipping);
            
        } catch (Exception e) {
            // 释放库存预留
            inventoryService.releaseReservation(reservation);
            throw e;
        }
    }
    
    private InventoryReservation reserveInventory(Order order) {
        List<InventoryItem> items = order.getItems().stream()
            .map(item -> new InventoryItem(item.getProductId(), item.getQuantity()))
            .collect(Collectors.toList());
        
        InventoryCheckResult checkResult = inventoryService.checkAvailability(items);
        
        if (!checkResult.isAllAvailable()) {
            throw new InsufficientInventoryException(checkResult.getUnavailableItems());
        }
        
        return inventoryService.reserve(items, order.getId());
    }
    
    private PriceBreakdown calculatePricing(Order order) {
        // 基础价格
        BigDecimal subtotal = pricingService.calculateSubtotal(order.getItems());
        
        // 应用折扣
        DiscountResult discount = pricingService.applyDiscounts(order, subtotal);
        
        // 计算税费
        BigDecimal tax = pricingService.calculateTax(discount.getFinalAmount(), order.getShippingAddress());
        
        // 计算运费
        BigDecimal shipping = pricingService.calculateShipping(order);
        
        return PriceBreakdown.builder()
            .subtotal(subtotal)
            .discount(discount.getDiscountAmount())
            .tax(tax)
            .shipping(shipping)
            .total(discount.getFinalAmount().add(tax).add(shipping))
            .build();
    }
    
    private PaymentResult processPayment(Order order, PriceBreakdown pricing) {
        PaymentRequest request = PaymentRequest.builder()
            .orderId(order.getId())
            .amount(pricing.getTotal())
            .currency(order.getCurrency())
            .paymentMethod(order.getPaymentMethod())
            .build();
        
        PaymentResult result = paymentService.process(request);
        
        if (!result.isSuccessful()) {
            throw new PaymentFailedException(result.getErrorMessage());
        }
        
        return result;
    }
    
    private ShippingInfo arrangeShipping(Order order) {
        ShippingRequest request = ShippingRequest.builder()
            .orderId(order.getId())
            .items(order.getItems())
            .address(order.getShippingAddress())
            .shippingMethod(order.getShippingMethod())
            .build();
        
        return shippingService.arrange(request);
    }
    
    private void sendNotifications(Order order, PaymentResult payment, ShippingInfo shipping) {
        // 异步发送通知
        CompletableFuture.runAsync(() -> {
            notificationService.sendOrderConfirmation(order);
            notificationService.sendPaymentReceipt(order, payment);
            notificationService.sendShippingNotification(order, shipping);
        });
    }
    
    private OrderResult buildSuccessResult(Order order, PriceBreakdown pricing, 
                                           PaymentResult payment, ShippingInfo shipping) {
        return OrderResult.builder()
            .orderId(order.getId())
            .status(OrderStatus.PROCESSED)
            .pricing(pricing)
            .paymentId(payment.getTransactionId())
            .trackingNumber(shipping.getTrackingNumber())
            .estimatedDelivery(shipping.getEstimatedDelivery())
            .processedAt(Instant.now())
            .build();
    }
}
```

## 22.4 架构层面重构

### 22.4.1 引入分层架构

```bash
claude "当前项目代码混乱，业务逻辑、数据访问、表示层代码混杂在一起。
请提供将其重构为标准分层架构的方案：
1. 表示层（Controller）
2. 业务层（Service）
3. 数据访问层（Repository）
4. 领域模型层（Domain）

包含：
1. 目录结构调整
2. 依赖关系规则
3. 迁移步骤
4. 示例代码"
```

分层架构方案：

```
重构后的目录结构：

src/
├── presentation/           # 表示层
│   ├── controllers/       # REST 控制器
│   │   ├── OrderController.java
│   │   └── UserController.java
│   ├── dto/               # 数据传输对象
│   │   ├── request/
│   │   └── response/
│   └── mappers/           # DTO 映射器
│
├── application/           # 应用层
│   ├── services/          # 应用服务
│   │   ├── OrderApplicationService.java
│   │   └── UserApplicationService.java
│   └── commands/          # 命令对象
│
├── domain/                # 领域层
│   ├── models/            # 领域模型
│   │   ├── Order.java
│   │   ├── User.java
│   │   └── valueobjects/
│   ├── services/          # 领域服务
│   ├── repositories/      # 仓储接口
│   └── events/            # 领域事件
│
└── infrastructure/        # 基础设施层
    ├── persistence/       # 持久化实现
    │   ├── repositories/  # 仓储实现
    │   └── entities/      # 数据库实体
    ├── external/          # 外部服务
    └── config/            # 配置
```

依赖关系规则：

```
┌─────────────────┐
│  Presentation   │ ──────┐
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│   Application   │ ──────┤
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│     Domain      │ ◄─────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Infrastructure  │
└─────────────────┘

规则：
1. 上层可以依赖下层
2. 下层不能依赖上层
3. Domain 层不依赖任何其他层
4. Infrastructure 实现 Domain 层定义的接口
```

### 22.4.2 引入依赖注入

```bash
claude "请将以下硬编码依赖的代码重构为使用依赖注入：

public class OrderService {
    private UserRepository userRepository = new UserRepositoryImpl();
    private EmailService emailService = new SmtpEmailService();
    private PaymentGateway paymentGateway = new StripePaymentGateway();
    
    public void processOrder(Order order) {
        User user = userRepository.findById(order.getUserId());
        paymentGateway.charge(user, order.getTotal());
        emailService.send(user.getEmail(), \"订单确认\", \"...\");
    }
}"
```

重构后的代码：

```java
// 接口定义
public interface UserRepository {
    Optional<User> findById(String id);
    User save(User user);
}

public interface EmailService {
    void send(String to, String subject, String body);
}

public interface PaymentGateway {
    PaymentResult charge(User user, BigDecimal amount);
}

// 服务实现
@Service
@RequiredArgsConstructor  // Lombok 自动生成构造器注入
public class OrderService {
    
    private final UserRepository userRepository;
    private final EmailService emailService;
    private final PaymentGateway paymentGateway;
    
    public void processOrder(Order order) {
        User user = userRepository.findById(order.getUserId())
            .orElseThrow(() -> new UserNotFoundException(order.getUserId()));
        
        paymentGateway.charge(user, order.getTotal());
        emailService.send(user.getEmail(), "订单确认", "...");
    }
}

// 配置类
@Configuration
public class ServiceConfig {
    
    @Bean
    @Profile("production")
    public EmailService productionEmailService() {
        return new SmtpEmailService();
    }
    
    @Bean
    @Profile("development")
    public EmailService developmentEmailService() {
        return new MockEmailService();  // 开发环境使用 Mock
    }
    
    @Bean
    @ConditionalOnProperty(name = "payment.gateway", havingValue = "stripe")
    public PaymentGateway stripePaymentGateway() {
        return new StripePaymentGateway();
    }
    
    @Bean
    @ConditionalOnProperty(name = "payment.gateway", havingValue = "paypal")
    public PaymentGateway paypalPaymentGateway() {
        return new PayPalPaymentGateway();
    }
}
```

## 22.5 重构验证与回归测试

### 22.5.1 验证重构正确性

```bash
claude "请帮我设计重构验证策略，确保重构后的代码行为与原代码一致：
1. 自动化测试验证
2. 手动测试检查点
3. 性能对比测试
4. 回滚计划"
```

验证策略：

```markdown
## 重构验证策略

### 1. 自动化测试验证

**单元测试**
- 所有新提取的方法必须有单元测试
- 测试覆盖率目标：核心业务逻辑 > 80%
- 使用 Mutation Testing 验证测试质量

**集成测试**
- 保持原有集成测试全部通过
- 新增 API 契约测试
- 数据库交互测试

**端到端测试**
- 核心用户流程自动化测试
- 使用 Selenium/Cypress 进行 UI 测试

### 2. 手动测试检查点

| 检查项 | 验证方法 | 负责人 |
|--------|---------|--------|
| 订单创建流程 | 创建各类型订单 | QA |
| 支付流程 | 测试各支付方式 | QA |
| 异常处理 | 模拟各类异常场景 | Dev |
| 边界条件 | 大数据量、并发测试 | Dev |

### 3. 性能对比测试

```bash
# 使用 JMeter 或 k6 进行性能测试
k6 run --vus 100 --duration 5m performance-test.js

# 对比指标
- 响应时间 P50/P95/P99
- 吞吐量 (RPS)
- 错误率
- 资源使用率
```

### 4. 回滚计划

**代码回滚**
- 使用 Git 标签标记重构前版本
- 准备回滚脚本

**数据回滚**
- 数据库迁移脚本支持回滚
- 备份关键数据

**发布策略**
- 使用灰度发布
- 先发布到 10% 流量
- 监控关键指标
- 逐步扩大发布范围
```

## 22.6 本章小结

本章详细介绍了如何使用 Claude Code 进行遗留代码重构：

1. **评估阶段**：使用 Claude Code 全面评估代码质量，识别问题和风险
2. **安全修复**：优先处理安全漏洞，如 SQL 注入、敏感信息泄露
3. **结构重构**：拆分大类、消除重复、重构长函数
4. **架构重构**：引入分层架构、依赖注入
5. **验证阶段**：建立测试安全网，确保重构正确性

重构的核心原则：

- **小步前进**：每次只做一个小改动，确保可以随时回滚
- **测试先行**：先建立测试安全网，再进行重构
- **持续验证**：每次改动后都运行测试，确保没有破坏现有功能
- **文档同步**：重构过程中同步更新文档

Claude Code 在重构过程中可以提供：
- 代码质量评估和问题识别
- 重构方案设计和代码生成
- 测试用例生成
- 文档更新辅助

通过系统性的重构方法和 Claude Code 的辅助，可以有效地改善遗留代码质量，降低维护成本，提高开发效率。
