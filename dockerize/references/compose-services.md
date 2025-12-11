# Docker Compose Service Templates

Ready-to-use service definitions for common infrastructure components.

**Modern Compose file conventions:**
- Use `compose.yml` (not `docker-compose.yml`) - the modern naming convention
- No `version` field needed - obsolete in Compose Specification
- Run with `docker compose up` (not `docker-compose up`)

## Databases

### PostgreSQL

```yaml
postgres:
  image: postgres:16-alpine
  restart: unless-stopped
  environment:
    POSTGRES_USER: ${POSTGRES_USER:-app}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-secret}
    POSTGRES_DB: ${POSTGRES_DB:-app}
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-app}"]
    interval: 10s
    timeout: 5s
    retries: 5
```

### MySQL

```yaml
mysql:
  image: mysql:8
  restart: unless-stopped
  environment:
    MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-rootsecret}
    MYSQL_DATABASE: ${MYSQL_DATABASE:-app}
    MYSQL_USER: ${MYSQL_USER:-app}
    MYSQL_PASSWORD: ${MYSQL_PASSWORD:-secret}
  ports:
    - "3306:3306"
  volumes:
    - mysql_data:/var/lib/mysql
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
    interval: 10s
    timeout: 5s
    retries: 5
```

### MongoDB

```yaml
mongodb:
  image: mongo:7
  restart: unless-stopped
  environment:
    MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER:-root}
    MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD:-secret}
    MONGO_INITDB_DATABASE: ${MONGO_DB:-app}
  ports:
    - "27017:27017"
  volumes:
    - mongo_data:/data/db
  healthcheck:
    test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
    interval: 10s
    timeout: 5s
    retries: 5
```

### SQLite (Volume Mount)

```yaml
# SQLite doesn't need a separate container - just mount a volume
app:
  volumes:
    - sqlite_data:/app/data
```

---

## Caching

### Redis

```yaml
redis:
  image: redis:7-alpine
  restart: unless-stopped
  command: redis-server --appendonly yes
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 10s
    timeout: 5s
    retries: 5
```

### Redis with Password

```yaml
redis:
  image: redis:7-alpine
  restart: unless-stopped
  command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD:-secret}
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
  healthcheck:
    test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD:-secret}", "ping"]
    interval: 10s
    timeout: 5s
    retries: 5
```

### Memcached

```yaml
memcached:
  image: memcached:1.6-alpine
  restart: unless-stopped
  ports:
    - "11211:11211"
  command: memcached -m 64
```

---

## Message Queues

### RabbitMQ

```yaml
rabbitmq:
  image: rabbitmq:3-management-alpine
  restart: unless-stopped
  environment:
    RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER:-guest}
    RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD:-guest}
  ports:
    - "5672:5672"   # AMQP
    - "15672:15672" # Management UI
  volumes:
    - rabbitmq_data:/var/lib/rabbitmq
  healthcheck:
    test: rabbitmq-diagnostics -q ping
    interval: 30s
    timeout: 10s
    retries: 5
```

### Kafka (with Zookeeper)

```yaml
zookeeper:
  image: confluentinc/cp-zookeeper:7.5.0
  restart: unless-stopped
  environment:
    ZOOKEEPER_CLIENT_PORT: 2181
    ZOOKEEPER_TICK_TIME: 2000
  volumes:
    - zookeeper_data:/var/lib/zookeeper/data
    - zookeeper_log:/var/lib/zookeeper/log

kafka:
  image: confluentinc/cp-kafka:7.5.0
  restart: unless-stopped
  depends_on:
    - zookeeper
  ports:
    - "9092:9092"
  environment:
    KAFKA_BROKER_ID: 1
    KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
    KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
  volumes:
    - kafka_data:/var/lib/kafka/data
```

### Kafka (KRaft - No Zookeeper)

```yaml
kafka:
  image: confluentinc/cp-kafka:7.5.0
  restart: unless-stopped
  ports:
    - "9092:9092"
  environment:
    KAFKA_NODE_ID: 1
    KAFKA_PROCESS_ROLES: broker,controller
    KAFKA_LISTENERS: PLAINTEXT://kafka:29092,CONTROLLER://kafka:29093,PLAINTEXT_HOST://0.0.0.0:9092
    KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
    KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:29093
    KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
    KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk
  volumes:
    - kafka_data:/var/lib/kafka/data
```

---

## Search

### Elasticsearch

```yaml
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
  restart: unless-stopped
  environment:
    - discovery.type=single-node
    - xpack.security.enabled=false
    - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
  ports:
    - "9200:9200"
    - "9300:9300"
  volumes:
    - elasticsearch_data:/usr/share/elasticsearch/data
  healthcheck:
    test: curl -s http://localhost:9200/_cluster/health | grep -vq '"status":"red"'
    interval: 30s
    timeout: 10s
    retries: 5
```

### OpenSearch

```yaml
opensearch:
  image: opensearchproject/opensearch:2.11.0
  restart: unless-stopped
  environment:
    - discovery.type=single-node
    - DISABLE_SECURITY_PLUGIN=true
    - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
  ports:
    - "9200:9200"
    - "9600:9600"
  volumes:
    - opensearch_data:/usr/share/opensearch/data
```

### Meilisearch

```yaml
meilisearch:
  image: getmeili/meilisearch:v1.5
  restart: unless-stopped
  environment:
    MEILI_MASTER_KEY: ${MEILI_MASTER_KEY:-masterkey}
  ports:
    - "7700:7700"
  volumes:
    - meilisearch_data:/meili_data
```

---

## Storage

### MinIO (S3-compatible)

```yaml
minio:
  image: minio/minio:latest
  restart: unless-stopped
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: ${MINIO_USER:-minioadmin}
    MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD:-minioadmin}
  ports:
    - "9000:9000"  # API
    - "9001:9001"  # Console
  volumes:
    - minio_data:/data
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
    interval: 30s
    timeout: 10s
    retries: 3
```

---

## Monitoring

### Prometheus

```yaml
prometheus:
  image: prom/prometheus:v2.47.0
  restart: unless-stopped
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    - prometheus_data:/prometheus
  command:
    - '--config.file=/etc/prometheus/prometheus.yml'
    - '--storage.tsdb.path=/prometheus'
```

### Grafana

```yaml
grafana:
  image: grafana/grafana:10.2.0
  restart: unless-stopped
  environment:
    GF_SECURITY_ADMIN_USER: ${GRAFANA_USER:-admin}
    GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD:-admin}
  ports:
    - "3001:3000"
  volumes:
    - grafana_data:/var/lib/grafana
```

### Jaeger (Tracing)

```yaml
jaeger:
  image: jaegertracing/all-in-one:1.51
  restart: unless-stopped
  ports:
    - "16686:16686"  # UI
    - "6831:6831/udp"  # Thrift compact
    - "14268:14268"  # Thrift HTTP
  environment:
    COLLECTOR_OTLP_ENABLED: true
```

---

## Reverse Proxy

### Traefik

```yaml
traefik:
  image: traefik:v2.10
  restart: unless-stopped
  command:
    - "--api.insecure=true"
    - "--providers.docker=true"
    - "--providers.docker.exposedbydefault=false"
    - "--entrypoints.web.address=:80"
  ports:
    - "80:80"
    - "8080:8080"  # Dashboard
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
```

### Nginx (Reverse Proxy)

```yaml
nginx:
  image: nginx:alpine
  restart: unless-stopped
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - ./certs:/etc/nginx/certs:ro
```

---

## Volumes Declaration

Add at the end of compose.yml:

```yaml
volumes:
  postgres_data:
  mysql_data:
  mongo_data:
  redis_data:
  rabbitmq_data:
  kafka_data:
  zookeeper_data:
  zookeeper_log:
  elasticsearch_data:
  opensearch_data:
  meilisearch_data:
  minio_data:
  prometheus_data:
  grafana_data:
```

---

## Network Configuration

For services that need to communicate:

```yaml
networks:
  default:
    name: app_network

# Or explicitly:
networks:
  backend:
    driver: bridge
  frontend:
    driver: bridge

services:
  app:
    networks:
      - backend
      - frontend
  db:
    networks:
      - backend
```

---

## Environment Variables Pattern

Create a `.env.example` file:

```env
# Database
POSTGRES_USER=app
POSTGRES_PASSWORD=changeme
POSTGRES_DB=app

# Redis
REDIS_PASSWORD=changeme

# App
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
```

And reference in compose.yml:

```yaml
services:
  app:
    env_file:
      - .env
```
