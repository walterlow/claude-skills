---
name: dockerize
description: Analyze repositories to detect tech stacks, dependencies, and services, then generate production-ready Dockerfiles and compose.yml configurations. This skill should be used when users ask to containerize a project, create Docker configs, or set up a development/production environment for their codebase.
---

# Dockerize Skill

This skill analyzes codebases to automatically generate Docker configurations for containerized deployment.

## Critical Docker Best Practices (MUST FOLLOW)

### 1. NEVER Use `latest` Tag

**WRONG:**
```dockerfile
FROM node:latest
FROM python:latest
FROM nginx:latest
```

**RIGHT:**
```dockerfile
FROM node:20.11.1-alpine3.19
FROM python:3.12.2-slim-bookworm
FROM nginx:1.25.4-alpine3.19
```

`latest` is a moving target. What works today may break tomorrow when the base image updates. Production deployments have failed due to unexpected base image changes. Pin versions for reproducible builds.

### 2. Use Minimal Base Images

Bloated images = larger attack surface, slower pulls, higher storage costs.

| Instead of | Use | Size Reduction |
|------------|-----|----------------|
| `ubuntu:22.04` | `python:3.12-slim` | ~90% smaller |
| `node:20` | `node:20-alpine` | ~80% smaller |
| `python:3.12` | `python:3.12-slim` | ~85% smaller |

For production, consider distroless images where possible.

### 3. NEVER Put Secrets in Dockerfiles

**CATASTROPHICALLY WRONG:**
```dockerfile
ENV AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
ENV AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/...
ARG NPM_TOKEN=abc123
```

Secrets baked into images are extractable by anyone with image access. They persist in layer history, registries, and CI logs.

**CORRECT - Use BuildKit secret mounts for build-time secrets:**
```dockerfile
# Secret available during build but NOT persisted in layer
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
```

**CORRECT - Pass secrets at runtime:**
```bash
docker run -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID myapp
```

**CORRECT - Use secrets management:**
- Docker Swarm secrets
- Kubernetes secrets
- HashiCorp Vault, AWS Secrets Manager

### 4. Optimize Layer Caching

Order by change frequency (least → most). Wrong order means npm/pip install runs from scratch on every code change.

**WRONG (cache invalidated on ANY file change):**
```dockerfile
COPY . .
RUN npm install
```

**RIGHT (npm install cached unless package.json changes):**
```dockerfile
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
```

This single change can cut build times from 8 minutes to under 1 minute.

### 5. Combine RUN Commands

Each instruction creates a layer. Cleanup in a later layer doesn't save space.

**WRONG (4 layers, cleanup doesn't work):**
```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get clean
```

**RIGHT (1 layer, cleanup actually saves space):**
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      wget \
    && rm -rf /var/lib/apt/lists/*
```

Use `--no-install-recommends` to skip suggested packages you don't need.

### 6. Run as Non-Root User

Default Docker containers run as root. Combined with a container escape vulnerability, this could compromise your host.

**WRONG:**
```dockerfile
CMD ["node", "server.js"]  # Runs as root
```

**RIGHT:**
```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --chown=appuser:appgroup . .
USER appuser
CMD ["node", "server.js"]
```

### 7. Always Include Health Checks

Without health checks, your orchestrator has no idea if your app is actually working vs stuck in a crash loop.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

Key points:
- `--start-period` gives your app time to initialize
- Check something meaningful (DB connectivity, not just "process exists")
- Keep checks lightweight (they run frequently)

### 8. Use Multi-Stage for Dev vs Prod

Don't ship debug tools, test suites, or dev dependencies to production.

```dockerfile
# Base stage
FROM node:20.11-alpine AS base
WORKDIR /app
COPY package*.json ./

# Development stage (with dev tools)
FROM base AS development
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

# Builder stage
FROM base AS builder
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage (minimal)
FROM node:20.11-alpine AS production
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
USER appuser
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

Build with target: `docker build --target production -t myapp:prod .`

### 9. Scan Images Regularly

That base image from last year has known CVEs. Update deliberately, not never.

```bash
# Docker Scout
docker scout cves myapp:latest

# Trivy
trivy image myapp:latest
```

Set up automated scanning in CI. Block deployments on critical vulnerabilities. Update base images monthly/quarterly with intentional testing.

### 10. Always Use .dockerignore

Without it, you're uploading your entire directory (including `.git`, `node_modules`, `.env` files) to the Docker daemon.

```
.git
node_modules
npm-debug.log
.env
.env.*
coverage
.nyc_output
*.md
.vscode
.idea
tests
__tests__
```

Be aggressive. If it's not needed in the final image, exclude it.

---

## When to Use

- User asks to "dockerize" a project or repository
- User needs a Dockerfile or compose.yml
- User wants to containerize their application
- User asks how to run their project in Docker
- User needs to set up a development environment image with Docker
- User needs to set up a product environment image with Docker
## Analysis Workflow

### Step 1: Analyze Repository Structure

To understand the project, examine these files and patterns:

**Package/Dependency Files:**
- `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` (Node.js)
- `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`, `poetry.lock` (Python)
- `go.mod`, `go.sum` (Go)
- `Cargo.toml`, `Cargo.lock` (Rust)
- `pom.xml`, `build.gradle`, `build.gradle.kts` (Java/Kotlin)
- `Gemfile`, `Gemfile.lock` (Ruby)
- `composer.json` (PHP)
- `*.csproj`, `*.fsproj`, `*.sln` (C#/.NET)

**Framework Detection Patterns:**
- **Next.js**: `next.config.js`, `.next/` directory, `next` in dependencies
- **React**: `react` in dependencies, `src/App.jsx` or `src/App.tsx`
- **Vue**: `vue.config.js`, `vue` in dependencies
- **Express**: `express` in dependencies
- **FastAPI**: `fastapi` in requirements, `uvicorn` usage
- **Django**: `django` in requirements, `manage.py`, `settings.py`
- **Flask**: `flask` in requirements
- **Spring Boot**: `spring-boot` in pom.xml/build.gradle
- **Rails**: `Gemfile` with `rails`, `config/routes.rb`

**Database/Service Detection:**
- **PostgreSQL**: `psycopg2`, `pg`, `postgres` in dependencies or connection strings
- **MySQL**: `mysql2`, `pymysql`, `mysql-connector` in dependencies
- **MongoDB**: `mongoose`, `pymongo`, `mongodb` in dependencies
- **Redis**: `redis`, `ioredis` in dependencies
- **Elasticsearch**: `elasticsearch`, `@elastic/elasticsearch` in dependencies
- **RabbitMQ**: `amqplib`, `pika` in dependencies
- **Kafka**: `kafka-python`, `kafkajs` in dependencies

### Step 2: Determine Entry Points and Build Commands

**Node.js Projects:**
- Check `package.json` scripts: `start`, `dev`, `build`, `serve`
- Look for `main` or `module` fields
- Identify if it's a monorepo (workspaces, lerna, nx, turborepo)

**Python Projects:**
- Check for `main.py`, `app.py`, `run.py`, `manage.py`
- Look at `pyproject.toml` [tool.poetry.scripts] or [project.scripts]
- Check for ASGI/WSGI entry points (uvicorn, gunicorn configs)

**Go Projects:**
- Look for `main.go` in root or `cmd/` directory
- Check `go.mod` for module name

**Rust Projects:**
- Check `Cargo.toml` for [[bin]] targets
- Look for `src/main.rs`

### Step 3: Generate Dockerfile

Follow these best practices when generating Dockerfiles:

1. **Use multi-stage builds** to minimize image size
2. **Pin base image versions** (e.g., `node:20-alpine` not `node:latest`)
3. **Copy dependency files first** to leverage layer caching
4. **Use non-root users** for security
5. **Set appropriate WORKDIR**
6. **Include health checks** where applicable
7. **Use .dockerignore** to exclude unnecessary files

Reference `references/dockerfile-templates.md` for language-specific templates.

### BuildKit Best Practices

Leverage BuildKit features for faster builds and better security:

1. **Add syntax directive** as the first line of every Dockerfile:
   ```dockerfile
   # syntax=docker/dockerfile:1
   ```

2. **Use cache mounts** to speed up repeated builds:
   - npm/yarn: `RUN --mount=type=cache,target=/root/.npm npm ci`
   - pip: `RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt`
   - go mod: `RUN --mount=type=cache,target=/go/pkg/mod go mod download`
   - cargo: `RUN --mount=type=cache,target=/usr/local/cargo/registry cargo build --release`

3. **Use secret mounts** for private dependencies (avoids secrets in image layers):
   ```dockerfile
   RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
   ```

4. **BuildKit is enabled by default** in Docker Engine v23.0+ and Docker Desktop

### Step 4: Generate compose.yml

Include detected services with sensible defaults:

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"  # Adjust based on detected port
    environment:
      - NODE_ENV=development
    depends_on:
      - db  # If database detected
    volumes:
      - .:/app  # For development hot-reload
      - /app/node_modules  # Prevent overwriting

  # Add detected services below
```

**Service Configuration Defaults:**

| Service | Image | Default Port | Volume |
|---------|-------|--------------|--------|
| PostgreSQL | postgres:16-alpine | 5432 | postgres_data:/var/lib/postgresql/data |
| MySQL | mysql:8 | 3306 | mysql_data:/var/lib/mysql |
| MongoDB | mongo:7 | 27017 | mongo_data:/data/db |
| Redis | redis:7-alpine | 6379 | redis_data:/data |
| Elasticsearch | elasticsearch:8.11.0 | 9200 | es_data:/usr/share/elasticsearch/data |

### Step 5: Generate Supporting Files

**Always create `.dockerignore`:**
```
node_modules/
__pycache__/
*.pyc
.git/
.env
.env.*
*.log
.DS_Store
Thumbs.db
dist/
build/
coverage/
.pytest_cache/
.mypy_cache/
target/
```

**For development, optionally create:**
- `compose.yml` for dev-specific settings
- `compose.prod.yml` for production configuration

## Output Format

When generating Docker configurations, provide:

1. **Analysis Summary**: Brief overview of detected tech stack
2. **Dockerfile**: With inline comments explaining key decisions
3. **compose.yml**: Ready to run with `docker compose up`
4. **.dockerignore**: Appropriate exclusions for the tech stack
5. **Usage Instructions**: Commands to build and run

## Example Usage Patterns

**User says:** "Dockerize this project"
- Run full analysis workflow
- Generate all configuration files
- Provide build/run instructions

**User says:** "Add Redis to my compose file"
- Read existing compose.yml
- Add Redis service with appropriate configuration
- Update app service with depends_on if needed

**User says:** "Optimize my Dockerfile"
- Read existing Dockerfile
- Suggest multi-stage build improvements
- Reduce image size
- Improve layer caching

## Important Considerations

- **Environment Variables**: Never hardcode secrets. Use environment variables or Docker secrets
- **Ports**: Detect actual ports from code (look for .listen(), PORT env var usage)
- **Health Checks**: Add appropriate health check endpoints when detected
- **Development vs Production**: Generate configs suitable for development by default, with notes on production hardening
