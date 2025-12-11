---
name: dockerize
description: Analyze repositories to detect tech stacks, dependencies, and services, then generate production-ready Dockerfiles and compose.yml configurations. This skill should be used when users ask to containerize a project, create Docker configs, or set up a development/production environment for their codebase.
---

# Dockerize Skill

This skill analyzes codebases to automatically generate Docker configurations for containerized deployment.

## When to Use

- User asks to "dockerize" a project or repository
- User needs a Dockerfile or compose.yml
- User wants to containerize their application
- User asks how to run their project in Docker
- User needs to set up a development environment with Docker

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
- `compose.override.yml` for dev-specific settings
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
