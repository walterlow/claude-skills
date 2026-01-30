# Dockerfile Templates Reference

This document contains production-ready Dockerfile templates for various tech stacks.

## Template Best Practices

**All templates follow these critical rules:**

1. **Pinned versions** - Never use `latest` or floating tags. Pin to specific versions (e.g., `node:20.11.1-alpine3.19`)
2. **Minimal base images** - Alpine or slim variants by default
3. **Non-root users** - All containers run as non-privileged users
4. **Health checks** - All long-running services include health checks
5. **Layer optimization** - Dependencies copied first, code last
6. **Combined RUN commands** - Cleanup in same layer as install

**BuildKit features used:**
- `# syntax=docker/dockerfile:1` enables latest Dockerfile syntax
- Cache mounts (`--mount=type=cache`) speed up repeated builds
- Secret mounts for build-time credentials (never bake secrets into images)
- BuildKit is enabled by default in Docker Engine v23.0+ and Docker Desktop

**Version pinning examples:**
```
# Look up current stable versions before generating:
# - Node.js: https://nodejs.org/en/about/releases/
# - Python: https://www.python.org/downloads/
# - Go: https://go.dev/dl/
# - Alpine: https://alpinelinux.org/releases/
```

## Node.js

### Node.js with npm (General)

```dockerfile
# syntax=docker/dockerfile:1

# Pin versions for reproducible builds
# Check https://nodejs.org/en/about/releases/ for current LTS
FROM node:20.11.1-alpine3.19 AS builder
WORKDIR /app

# Copy package files FIRST for layer caching
COPY package*.json ./

# Install dependencies with cache mount
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Copy source LAST (changes frequently)
COPY . .

# Build if needed (uncomment for TypeScript/build step)
# RUN npm run build

# Production stage - minimal image
FROM node:20.11.1-alpine3.19 AS runner
WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 appuser

# Copy from builder
COPY --from=builder --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:nodejs /app .

USER appuser

EXPOSE 3000

# Health check - adjust endpoint as needed
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "index.js"]
```

### Next.js (Standalone Output)

```dockerfile
# syntax=docker/dockerfile:1

# Pin to specific version - check nodejs.org for current LTS
FROM node:20.11.1-alpine3.19 AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=cache,target=/root/.yarn \
    --mount=type=cache,target=/root/.local/share/pnpm/store \
    if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
    else echo "Lockfile not found." && exit 1; \
    fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

RUN \
  if [ -f yarn.lock ]; then yarn run build; \
  elif [ -f package-lock.json ]; then npm run build; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm run build; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Production image - minimal
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user - combine RUN commands for smaller layers
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs && \
    mkdir .next && \
    chown nextjs:nodejs .next

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
```

### Express/Fastify API

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version
FROM node:20.11.1-alpine3.19 AS builder
WORKDIR /app

# Dependencies first for layer caching
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Source code last
COPY . .
RUN npm run build 2>/dev/null || true

# Production stage
FROM node:20.11.1-alpine3.19
WORKDIR /app

# Create user in single layer
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001

COPY --from=builder --chown=nodejs:nodejs /app/package*.json ./
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist 2>/dev/null || true
COPY --from=builder --chown=nodejs:nodejs /app/src ./src 2>/dev/null || true

USER nodejs

EXPOSE 3000

# Health check is essential for orchestration
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

---

## Python

### Python with pip (General)

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version - check python.org/downloads for current stable
FROM python:3.12.2-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies - combine RUN commands
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Dependencies first for layer caching
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Production stage - minimal
FROM python:3.12.2-slim-bookworm

WORKDIR /app

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Copy application last (changes most frequently)
COPY --chown=appuser:appuser . .

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["python", "main.py"]
```

### FastAPI with Uvicorn

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version
FROM python:3.12.2-slim-bookworm AS builder

WORKDIR /app

# Combine apt commands in single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Dependencies first
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Production stage
FROM python:3.12.2-slim-bookworm

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN useradd --create-home appuser
USER appuser

# Code last
COPY --chown=appuser:appuser . .

EXPOSE 8000

# Health check verifies actual endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Django

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version
FROM python:3.12.2-slim-bookworm AS builder

WORKDIR /app

# Combine apt commands
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Dependencies first
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Production stage
FROM python:3.12.2-slim-bookworm

WORKDIR /app

# Runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN useradd --create-home appuser
USER appuser

# Code last
COPY --chown=appuser:appuser . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "config.wsgi:application"]
```

### Python ML/Data Science (with CUDA support option)

```dockerfile
# syntax=docker/dockerfile:1

# For CPU-only - pin specific version
FROM python:3.11.8-slim-bookworm AS base

# For GPU (uncomment and use instead) - pin CUDA version
# FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04 AS base
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Combine apt commands for smaller layers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Dependencies first for caching
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Non-root user for security
RUN useradd --create-home appuser
USER appuser

# Code last
COPY --chown=appuser:appuser . .

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["python", "main.py"]
```

---

## Go

### Go (Multi-stage)

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version - check go.dev/dl for current stable
FROM golang:1.22.1-alpine3.19 AS builder

WORKDIR /app

# Install certificates for HTTPS
RUN apk add --no-cache ca-certificates

# Dependencies first for caching
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Code last
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server .

# Minimal production image (scratch = no OS, smallest possible)
FROM scratch

WORKDIR /app

# Copy certificates for HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy binary
COPY --from=builder /app/server .

EXPOSE 8080

# Note: scratch images can't run shell commands for health checks
# Use orchestrator health checks (Kubernetes probes) instead
ENTRYPOINT ["/app/server"]
```

### Go with CGO

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific versions
FROM golang:1.22.1-alpine3.19 AS builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev

# Dependencies first
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Code last
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app/server .

# Pin Alpine version
FROM alpine:3.19.1

WORKDIR /app

RUN apk add --no-cache ca-certificates

# Non-root user
RUN adduser -D -u 1001 appuser
USER appuser

COPY --from=builder /app/server .

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["./server"]
```

---

## Rust

### Rust (Multi-stage)

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version
FROM rust:1.75.0-alpine3.19 AS builder

WORKDIR /app

RUN apk add --no-cache musl-dev

# Dependencies first - create dummy src for caching
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs

# Build dependencies (cached unless Cargo.toml changes)
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release

# Now build actual application
COPY . .
RUN touch src/main.rs
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release && \
    cp target/release/app /app/app-binary

# Pin Alpine version
FROM alpine:3.19.1

WORKDIR /app

# Non-root user
RUN adduser -D -u 1001 appuser
USER appuser

COPY --from=builder /app/app-binary ./app

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["./app"]
```

---

## Java

### Spring Boot with Maven

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version - check Adoptium for current releases
FROM eclipse-temurin:21.0.2_13-jdk-alpine AS builder

WORKDIR /app

# Dependencies first
COPY .mvn/ .mvn
COPY mvnw pom.xml ./
RUN --mount=type=cache,target=/root/.m2 \
    ./mvnw dependency:go-offline

# Code last
COPY src ./src
RUN --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests

# Production - JRE only (smaller)
FROM eclipse-temurin:21.0.2_13-jre-alpine

WORKDIR /app

# Non-root user
RUN addgroup -g 1001 -S spring && adduser -S spring -u 1001 -G spring
USER spring

COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8080

# Health check using Spring Actuator
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Spring Boot with Gradle

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version
FROM eclipse-temurin:21.0.2_13-jdk-alpine AS builder

WORKDIR /app

# Dependencies first
COPY gradle gradle
COPY gradlew build.gradle* settings.gradle* ./
RUN --mount=type=cache,target=/root/.gradle \
    ./gradlew dependencies --no-daemon

# Code last
COPY src ./src
RUN --mount=type=cache,target=/root/.gradle \
    ./gradlew bootJar --no-daemon

# Production - JRE only
FROM eclipse-temurin:21.0.2_13-jre-alpine

WORKDIR /app

# Non-root user
RUN addgroup -g 1001 -S spring && adduser -S spring -u 1001 -G spring
USER spring

COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## .NET

### ASP.NET Core

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version - check mcr.microsoft.com for releases
FROM mcr.microsoft.com/dotnet/sdk:8.0.201 AS builder

WORKDIR /app

# Dependencies first
COPY *.csproj ./
RUN --mount=type=cache,target=/root/.nuget/packages \
    dotnet restore

# Code last
COPY . ./
RUN --mount=type=cache,target=/root/.nuget/packages \
    dotnet publish -c Release -o /app/publish

# Production - runtime only (smaller)
FROM mcr.microsoft.com/dotnet/aspnet:8.0.2

WORKDIR /app

# Non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

COPY --from=builder /app/publish .

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["dotnet", "App.dll"]
```

---

## Ruby

### Ruby on Rails

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version
FROM ruby:3.3.0-alpine3.19 AS builder

WORKDIR /app

# System deps in single layer
RUN apk add --no-cache build-base postgresql-dev nodejs yarn

# Dependencies first
COPY Gemfile Gemfile.lock ./
RUN --mount=type=cache,target=/root/.bundle \
    bundle config set --local deployment 'true' \
    && bundle config set --local without 'development test' \
    && bundle install

COPY package.json yarn.lock ./
RUN --mount=type=cache,target=/root/.yarn \
    yarn install --frozen-lockfile

# Code last
COPY . .
RUN RAILS_ENV=production bundle exec rake assets:precompile

# Production - pin version
FROM ruby:3.3.0-alpine3.19

WORKDIR /app

# Runtime deps only
RUN apk add --no-cache postgresql-client nodejs tzdata

# Non-root user
RUN adduser -D -u 1001 rails
USER rails

COPY --from=builder --chown=rails:rails /app /app

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]
```

---

## PHP

### PHP with Laravel

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific version
FROM composer:2.7.1 AS composer

WORKDIR /app

# Dependencies first
COPY composer.json composer.lock ./
RUN --mount=type=cache,target=/root/.composer/cache \
    composer install --no-dev --no-scripts --no-autoloader

# Code last
COPY . .
RUN composer dump-autoload --optimize

# Production - pin version
FROM php:8.3.3-fpm-alpine3.19

WORKDIR /app

# Combine system deps in single layer
RUN apk add --no-cache nginx supervisor && \
    docker-php-ext-install pdo pdo_mysql opcache

COPY --from=composer /app /app

RUN chown -R www-data:www-data /app/storage /app/bootstrap/cache

COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

---

## Static Sites / Frontend

### Static Site (Nginx)

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific versions
FROM node:20.11.1-alpine3.19 AS builder

WORKDIR /app

# Dependencies first
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Code last
COPY . .
RUN npm run build

# Pin nginx version
FROM nginx:1.25.4-alpine3.19

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

### React/Vue/Angular SPA

```dockerfile
# syntax=docker/dockerfile:1

# Pin specific versions
FROM node:20.11.1-alpine3.19 AS builder

WORKDIR /app

# Dependencies first
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Code last
COPY . .
RUN npm run build

# Pin nginx version
FROM nginx:1.25.4-alpine3.19

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# SPA routing support
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```
