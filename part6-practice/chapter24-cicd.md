# 第24章：CI/CD 流水线集成

持续集成（CI）和持续部署（CD）是现代软件开发的核心实践。通过自动化的构建、测试和部署流程，团队可以更快、更可靠地交付软件。本章将介绍如何使用 Claude Code 辅助搭建和优化 CI/CD 流水线。

## 24.1 CI/CD 基础概念

### 24.1.1 持续集成与持续部署

**持续集成（CI）** 是指开发人员频繁地将代码变更合并到主分支，每次合并都会触发自动化构建和测试，以尽早发现集成问题。

**持续部署（CD）** 包含两个层次：
- **持续交付（Continuous Delivery）**：代码变更自动构建、测试，并准备好随时部署到生产环境
- **持续部署（Continuous Deployment）**：代码变更自动部署到生产环境，无需人工干预

### 24.1.2 CI/CD 流水线阶段

```mermaid
flowchart LR
    A[代码提交] --> B[构建 Build]
    B --> C[测试 Test]
    C --> D[部署 Deploy]
    D --> E[监控 Monitor]
```

## 24.2 GitHub Actions 配置

### 24.2.1 基础工作流配置

```bash
claude "请为一个 Node.js + React 全栈项目创建 GitHub Actions 工作流，包含：
1. 代码检查（ESLint）
2. 单元测试
3. 构建
4. Docker 镜像构建
5. 部署到测试环境"
```

完整的 GitHub Actions 配置：

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # 代码质量检查
  lint:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ESLint
        run: npm run lint
      
      - name: Run Prettier check
        run: npm run format:check
      
      - name: TypeScript type check
        run: npm run type-check

  # 单元测试
  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:unit -- --coverage
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          fail_ci_if_error: true

  # 集成测试
  integration-test:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run database migrations
        run: npm run db:migrate
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
      
      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379

  # 构建应用
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [test, integration-test]
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build application
        run: npm run build
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/
          retention-days: 7

  # 构建 Docker 镜像
  docker:
    name: Docker Build
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push'
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: build
          path: dist/
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix=
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # 部署到测试环境
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: docker
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - name: Deploy to staging server
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.STAGING_SSH_KEY }}
          script: |
            cd /opt/app
            docker compose pull
            docker compose up -d
            docker system prune -f

  # 部署到生产环境
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: docker
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://www.example.com
    
    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.PRODUCTION_HOST }}
          username: ${{ secrets.PRODUCTION_USER }}
          key: ${{ secrets.PRODUCTION_SSH_KEY }}
          script: |
            cd /opt/app
            docker compose pull
            docker compose up -d --no-deps app
            docker system prune -f
```

### 24.2.2 矩阵构建策略

```bash
claude "请配置 GitHub Actions 矩阵构建，支持：
1. 多 Node.js 版本测试
2. 多操作系统测试
3. 失败快速终止"
```

```yaml
jobs:
  test-matrix:
    name: Test (${{ matrix.os }}, Node ${{ matrix.node }})
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: true
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [16, 18, 20]
        exclude:
          - os: macos-latest
            node: 16
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
```

## 24.3 GitLab CI/CD 配置

```bash
claude "请为同一项目创建 GitLab CI/CD 配置，包含相同的流水线阶段"
```

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - docker
  - deploy

variables:
  NODE_VERSION: "18"
  DOCKER_DRIVER: overlay2

# 缓存配置
.node_cache: &node_cache
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - node_modules/
    policy: pull-push

# 代码检查
lint:
  stage: lint
  image: node:${NODE_VERSION}
  <<: *node_cache
  script:
    - npm ci
    - npm run lint
    - npm run format:check
    - npm run type-check

# 单元测试
unit-test:
  stage: test
  image: node:${NODE_VERSION}
  <<: *node_cache
  script:
    - npm ci
    - npm run test:unit -- --coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

# 集成测试
integration-test:
  stage: test
  image: node:${NODE_VERSION}
  services:
    - postgres:15-alpine
    - redis:7-alpine
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    DATABASE_URL: postgresql://test:test@postgres:5432/testdb
    REDIS_URL: redis://redis:6379
  <<: *node_cache
  script:
    - npm ci
    - npm run db:migrate
    - npm run test:integration

# 构建
build:
  stage: build
  image: node:${NODE_VERSION}
  <<: *node_cache
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

# Docker 构建
docker-build:
  stage: docker
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
    - develop

# 部署到测试环境
deploy-staging:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client
    - eval $(ssh-agent -s)
    - echo "$STAGING_SSH_KEY" | ssh-add -
  script:
    - ssh -o StrictHostKeyChecking=no $STAGING_USER@$STAGING_HOST "
        cd /opt/app &&
        docker compose pull &&
        docker compose up -d"
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

# 部署到生产环境
deploy-production:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client
    - eval $(ssh-agent -s)
    - echo "$PRODUCTION_SSH_KEY" | ssh-add -
  script:
    - ssh -o StrictHostKeyChecking=no $PRODUCTION_USER@$PRODUCTION_HOST "
        cd /opt/app &&
        docker compose pull &&
        docker compose up -d"
  environment:
    name: production
    url: https://www.example.com
  only:
    - main
  when: manual
```

## 24.4 Claude Code 在 CI/CD 中的应用

### 24.4.1 自动化代码审查

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Claude Code
        run: npm install -g @anthropic-ai/claude-code
      
      - name: Get changed files
        id: changed
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | grep -E '\.(js|ts|jsx|tsx)$' | tr '\n' ' ')
          echo "files=$FILES" >> $GITHUB_OUTPUT
      
      - name: AI Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          for file in ${{ steps.changed.outputs.files }}; do
            echo "Reviewing $file..."
            claude -p "请审查文件 $file 的代码变更，关注安全性、性能和代码质量" >> review.md
          done
      
      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

### 24.4.2 自动生成变更日志

```yaml
# .github/workflows/changelog.yml
name: Generate Changelog

on:
  release:
    types: [created]

jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Claude Code
        run: npm install -g @anthropic-ai/claude-code
      
      - name: Generate changelog
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          COMMITS=$(git log --oneline $(git describe --tags --abbrev=0 HEAD^)..HEAD)
          echo "$COMMITS" | claude -p "请根据以下 Git 提交记录生成用户友好的变更日志，按功能、修复、改进分类" > CHANGELOG_NEW.md
      
      - name: Update Release Notes
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const changelog = fs.readFileSync('CHANGELOG_NEW.md', 'utf8');
            github.rest.repos.updateRelease({
              owner: context.repo.owner,
              repo: context.repo.repo,
              release_id: context.payload.release.id,
              body: changelog
            });
```

## 24.5 部署策略

### 24.5.1 蓝绿部署

```bash
claude "请设计蓝绿部署策略的实现方案，使用 Docker 和 Nginx"
```

```yaml
# docker-compose.blue-green.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app-blue
      - app-green

  app-blue:
    image: ${IMAGE_NAME}:${BLUE_VERSION}
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  app-green:
    image: ${IMAGE_NAME}:${GREEN_VERSION}
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 24.5.2 金丝雀发布

```yaml
# 金丝雀发布脚本
name: Canary Deployment

on:
  workflow_dispatch:
    inputs:
      canary_percentage:
        description: 'Canary traffic percentage'
        required: true
        default: '10'

jobs:
  canary:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy canary version
        run: |
          # 更新负载均衡器权重
          kubectl patch service app-service -p '{
            "spec": {
              "selector": {
                "version": "canary"
              }
            }
          }'
      
      - name: Wait and monitor
        run: |
          sleep 300  # 等待 5 分钟
          # 检查错误率
          ERROR_RATE=$(curl -s "$METRICS_URL/error_rate")
          if [ $(echo "$ERROR_RATE > 0.01" | bc) -eq 1 ]; then
            echo "Error rate too high, rolling back"
            exit 1
          fi
      
      - name: Promote or rollback
        if: success()
        run: |
          # 逐步增加流量
          for pct in 25 50 75 100; do
            kubectl set env deployment/app CANARY_WEIGHT=$pct
            sleep 60
          done
```

## 24.6 本章小结

本章详细介绍了 CI/CD 流水线的搭建和优化：

1. **CI/CD 基础**：理解持续集成和持续部署的概念和价值
2. **GitHub Actions**：配置完整的 CI/CD 工作流
3. **GitLab CI/CD**：使用 GitLab 的流水线配置
4. **Claude Code 集成**：在 CI/CD 中使用 AI 进行代码审查和文档生成
5. **部署策略**：实现蓝绿部署和金丝雀发布

关键要点：
- 自动化是 CI/CD 的核心，减少人工干预
- 测试是质量门禁，确保代码质量
- 渐进式部署降低发布风险
- 监控和回滚机制保障生产稳定性
