#!/usr/bin/env python3
"""
Analyze a repository to detect tech stack, dependencies, and services.
Outputs a JSON report for use in Dockerfile generation.

Usage:
    python analyze_repo.py [path_to_repo]

If no path is provided, analyzes the current directory.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


def detect_node_project(repo_path: Path) -> dict[str, Any] | None:
    """Detect Node.js project and extract details."""
    package_json = repo_path / "package.json"
    if not package_json.exists():
        return None

    try:
        with open(package_json, "r", encoding="utf-8") as f:
            pkg = json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

    # Detect framework
    framework = None
    if "next" in deps:
        framework = "nextjs"
    elif "nuxt" in deps:
        framework = "nuxt"
    elif "@angular/core" in deps:
        framework = "angular"
    elif "vue" in deps:
        framework = "vue"
    elif "react" in deps:
        framework = "react"
    elif "express" in deps:
        framework = "express"
    elif "fastify" in deps:
        framework = "fastify"
    elif "koa" in deps:
        framework = "koa"
    elif "hono" in deps:
        framework = "hono"

    # Detect package manager
    package_manager = "npm"
    if (repo_path / "pnpm-lock.yaml").exists():
        package_manager = "pnpm"
    elif (repo_path / "yarn.lock").exists():
        package_manager = "yarn"
    elif (repo_path / "bun.lockb").exists():
        package_manager = "bun"

    # Get scripts
    scripts = pkg.get("scripts", {})

    # Detect TypeScript
    is_typescript = "typescript" in deps or (repo_path / "tsconfig.json").exists()

    return {
        "runtime": "node",
        "framework": framework,
        "package_manager": package_manager,
        "scripts": scripts,
        "typescript": is_typescript,
        "node_version": pkg.get("engines", {}).get("node"),
        "dependencies": list(deps.keys()),
    }


def detect_python_project(repo_path: Path) -> dict[str, Any] | None:
    """Detect Python project and extract details."""
    indicators = [
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "Pipfile",
        "poetry.lock",
    ]

    if not any((repo_path / ind).exists() for ind in indicators):
        return None

    deps = []
    framework = None
    package_manager = "pip"

    # Check pyproject.toml first
    pyproject = repo_path / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text(encoding="utf-8")
            if "[tool.poetry]" in content:
                package_manager = "poetry"
            elif "[tool.pdm]" in content:
                package_manager = "pdm"
            elif "[project]" in content:
                package_manager = "pip"  # PEP 621

            # Extract dependencies (simplified)
            dep_match = re.findall(r'^\s*["\']?([a-zA-Z0-9_-]+)', content, re.MULTILINE)
            deps.extend(dep_match)
        except IOError:
            pass

    # Check requirements.txt
    requirements = repo_path / "requirements.txt"
    if requirements.exists():
        try:
            content = requirements.read_text(encoding="utf-8")
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    # Extract package name
                    match = re.match(r'^([a-zA-Z0-9_-]+)', line)
                    if match:
                        deps.append(match.group(1).lower())
        except IOError:
            pass

    # Check Pipfile
    if (repo_path / "Pipfile").exists():
        package_manager = "pipenv"

    # Detect framework from dependencies
    deps_lower = [d.lower() for d in deps]
    if "fastapi" in deps_lower:
        framework = "fastapi"
    elif "django" in deps_lower:
        framework = "django"
    elif "flask" in deps_lower:
        framework = "flask"
    elif "starlette" in deps_lower:
        framework = "starlette"
    elif "tornado" in deps_lower:
        framework = "tornado"
    elif "streamlit" in deps_lower:
        framework = "streamlit"
    elif "gradio" in deps_lower:
        framework = "gradio"

    # Detect entry point
    entry_point = None
    for candidate in ["main.py", "app.py", "run.py", "server.py", "manage.py"]:
        if (repo_path / candidate).exists():
            entry_point = candidate
            break

    # Check for ML/Data science
    is_ml = any(d in deps_lower for d in ["torch", "tensorflow", "keras", "scikit-learn", "pandas", "numpy"])

    return {
        "runtime": "python",
        "framework": framework,
        "package_manager": package_manager,
        "entry_point": entry_point,
        "dependencies": list(set(deps)),
        "is_ml": is_ml,
    }


def detect_go_project(repo_path: Path) -> dict[str, Any] | None:
    """Detect Go project and extract details."""
    go_mod = repo_path / "go.mod"
    if not go_mod.exists():
        return None

    try:
        content = go_mod.read_text(encoding="utf-8")
    except IOError:
        return None

    # Extract module name
    module_match = re.search(r'^module\s+(\S+)', content, re.MULTILINE)
    module_name = module_match.group(1) if module_match else None

    # Extract Go version
    version_match = re.search(r'^go\s+(\d+\.\d+)', content, re.MULTILINE)
    go_version = version_match.group(1) if version_match else None

    # Find main.go location
    entry_point = None
    if (repo_path / "main.go").exists():
        entry_point = "."
    else:
        cmd_dir = repo_path / "cmd"
        if cmd_dir.exists():
            for sub in cmd_dir.iterdir():
                if sub.is_dir() and (sub / "main.go").exists():
                    entry_point = f"./cmd/{sub.name}"
                    break

    return {
        "runtime": "go",
        "module": module_name,
        "go_version": go_version,
        "entry_point": entry_point,
    }


def detect_rust_project(repo_path: Path) -> dict[str, Any] | None:
    """Detect Rust project and extract details."""
    cargo_toml = repo_path / "Cargo.toml"
    if not cargo_toml.exists():
        return None

    try:
        content = cargo_toml.read_text(encoding="utf-8")
    except IOError:
        return None

    # Extract package name
    name_match = re.search(r'^name\s*=\s*"([^"]+)"', content, re.MULTILINE)
    package_name = name_match.group(1) if name_match else None

    # Check if it's a workspace
    is_workspace = "[workspace]" in content

    return {
        "runtime": "rust",
        "package_name": package_name,
        "is_workspace": is_workspace,
    }


def detect_java_project(repo_path: Path) -> dict[str, Any] | None:
    """Detect Java/Kotlin project and extract details."""
    pom = repo_path / "pom.xml"
    gradle = repo_path / "build.gradle"
    gradle_kts = repo_path / "build.gradle.kts"

    if not any([pom.exists(), gradle.exists(), gradle_kts.exists()]):
        return None

    build_tool = None
    framework = None

    if pom.exists():
        build_tool = "maven"
        try:
            content = pom.read_text(encoding="utf-8")
            if "spring-boot" in content:
                framework = "spring-boot"
            elif "quarkus" in content:
                framework = "quarkus"
            elif "micronaut" in content:
                framework = "micronaut"
        except IOError:
            pass
    elif gradle.exists() or gradle_kts.exists():
        build_tool = "gradle"
        gradle_file = gradle_kts if gradle_kts.exists() else gradle
        try:
            content = gradle_file.read_text(encoding="utf-8")
            if "spring-boot" in content or "org.springframework.boot" in content:
                framework = "spring-boot"
            elif "quarkus" in content:
                framework = "quarkus"
            elif "micronaut" in content:
                framework = "micronaut"
        except IOError:
            pass

    return {
        "runtime": "java",
        "build_tool": build_tool,
        "framework": framework,
    }


def detect_dotnet_project(repo_path: Path) -> dict[str, Any] | None:
    """Detect .NET project and extract details."""
    csproj_files = list(repo_path.glob("*.csproj"))
    fsproj_files = list(repo_path.glob("*.fsproj"))
    sln_files = list(repo_path.glob("*.sln"))

    if not any([csproj_files, fsproj_files, sln_files]):
        return None

    language = "csharp" if csproj_files else "fsharp" if fsproj_files else "unknown"

    # Try to detect framework
    framework = None
    project_file = csproj_files[0] if csproj_files else fsproj_files[0] if fsproj_files else None

    if project_file:
        try:
            content = project_file.read_text(encoding="utf-8")
            if "Microsoft.AspNetCore" in content:
                framework = "aspnet"
            elif "Microsoft.NET.Sdk.Web" in content:
                framework = "aspnet"
            elif "Microsoft.NET.Sdk.Worker" in content:
                framework = "worker"
        except IOError:
            pass

    return {
        "runtime": "dotnet",
        "language": language,
        "framework": framework,
        "project_file": str(project_file) if project_file else None,
    }


def detect_services(repo_path: Path) -> list[dict[str, Any]]:
    """Detect databases and services from code and config."""
    services = []

    # Files to scan for connection strings and imports
    scan_extensions = {".py", ".js", ".ts", ".go", ".java", ".cs", ".rb", ".php"}
    config_files = ["compose.yml", "compose.yaml", "docker-compose.yml", "docker-compose.yaml", ".env", ".env.example"]

    # Patterns to detect services
    service_patterns = {
        "postgresql": [
            r"postgres://", r"postgresql://", r"psycopg2", r"pg\.", r"PG::",
            r"POSTGRES", r"5432", r'"pg"', r"asyncpg"
        ],
        "mysql": [
            r"mysql://", r"mysql2", r"pymysql", r"MySql", r"MYSQL", r"3306"
        ],
        "mongodb": [
            r"mongodb://", r"mongoose", r"pymongo", r"MongoClient", r"MONGO", r"27017"
        ],
        "redis": [
            r"redis://", r"ioredis", r"redis\.", r"Redis\(", r"REDIS", r"6379"
        ],
        "elasticsearch": [
            r"elasticsearch", r"@elastic", r"ELASTICSEARCH", r"9200"
        ],
        "rabbitmq": [
            r"amqp://", r"amqplib", r"pika", r"RabbitMQ", r"RABBITMQ", r"5672"
        ],
        "kafka": [
            r"kafka", r"kafkajs", r"kafka-python", r"KAFKA", r"9092"
        ],
        "memcached": [
            r"memcached", r"pylibmc", r"MEMCACHED", r"11211"
        ],
        "minio": [
            r"minio", r"MINIO", r"9000"
        ],
    }

    detected = set()

    # Scan source files
    for ext in scan_extensions:
        for file_path in repo_path.rglob(f"*{ext}"):
            # Skip node_modules, vendor, etc.
            if any(part in str(file_path) for part in ["node_modules", "vendor", ".git", "__pycache__", "venv"]):
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                for service, patterns in service_patterns.items():
                    if service not in detected:
                        for pattern in patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                detected.add(service)
                                break
            except IOError:
                continue

    # Scan config files
    for config in config_files:
        config_path = repo_path / config
        if config_path.exists():
            try:
                content = config_path.read_text(encoding="utf-8")
                for service, patterns in service_patterns.items():
                    if service not in detected:
                        for pattern in patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                detected.add(service)
                                break
            except IOError:
                continue

    # Build service list with defaults
    service_defaults = {
        "postgresql": {"image": "postgres:16-alpine", "port": 5432},
        "mysql": {"image": "mysql:8", "port": 3306},
        "mongodb": {"image": "mongo:7", "port": 27017},
        "redis": {"image": "redis:7-alpine", "port": 6379},
        "elasticsearch": {"image": "elasticsearch:8.11.0", "port": 9200},
        "rabbitmq": {"image": "rabbitmq:3-management-alpine", "port": 5672},
        "kafka": {"image": "confluentinc/cp-kafka:7.5.0", "port": 9092},
        "memcached": {"image": "memcached:1.6-alpine", "port": 11211},
        "minio": {"image": "minio/minio:latest", "port": 9000},
    }

    for service in detected:
        defaults = service_defaults.get(service, {})
        services.append({
            "name": service,
            "image": defaults.get("image"),
            "port": defaults.get("port"),
        })

    return services


def detect_ports(repo_path: Path) -> list[int]:
    """Detect ports used by the application."""
    ports = set()
    port_patterns = [
        r'\.listen\s*\(\s*(\d+)',  # .listen(3000)
        r'PORT\s*[=:]\s*(\d+)',    # PORT=3000 or PORT: 3000
        r'port\s*[=:]\s*(\d+)',    # port=3000 or port: 3000
        r'--port\s+(\d+)',          # --port 3000
        r'-p\s+(\d+)',              # -p 3000
    ]

    scan_extensions = {".py", ".js", ".ts", ".go", ".java", ".yml", ".yaml", ".env"}

    for ext in scan_extensions:
        for file_path in repo_path.rglob(f"*{ext}"):
            if any(part in str(file_path) for part in ["node_modules", "vendor", ".git", "__pycache__"]):
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                for pattern in port_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        port = int(match)
                        if 1000 <= port <= 65535:
                            ports.add(port)
            except (IOError, ValueError):
                continue

    return sorted(ports)


def analyze_repo(repo_path: str | Path) -> dict[str, Any]:
    """Main analysis function."""
    repo_path = Path(repo_path).resolve()

    if not repo_path.exists():
        return {"error": f"Path does not exist: {repo_path}"}

    if not repo_path.is_dir():
        return {"error": f"Path is not a directory: {repo_path}"}

    result = {
        "path": str(repo_path),
        "name": repo_path.name,
        "runtime": None,
        "services": [],
        "ports": [],
    }

    # Detect primary runtime/framework
    detectors = [
        detect_node_project,
        detect_python_project,
        detect_go_project,
        detect_rust_project,
        detect_java_project,
        detect_dotnet_project,
    ]

    for detector in detectors:
        detected = detector(repo_path)
        if detected:
            result.update(detected)
            break

    # Detect services
    result["services"] = detect_services(repo_path)

    # Detect ports
    result["ports"] = detect_ports(repo_path)

    # Check for existing Docker files
    result["existing_docker"] = {
        "dockerfile": (repo_path / "Dockerfile").exists(),
        "docker_compose": (repo_path / "compose.yml").exists() or (repo_path / "compose.yaml").exists() or (repo_path / "docker-compose.yml").exists() or (repo_path / "docker-compose.yaml").exists(),
        "dockerignore": (repo_path / ".dockerignore").exists(),
    }

    return result


def main():
    """CLI entry point."""
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = analyze_repo(repo_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
