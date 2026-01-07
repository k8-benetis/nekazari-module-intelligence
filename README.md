# Nekazari Intelligence Module

**Standalone AI/ML module for Nekazari platform** - Independent repository for analysis and prediction services.

This module follows the [Nekazari Module Template](../module-template/README.md) structure for consistency with the platform's module ecosystem.

## License

Licensed under the [Apache License 2.0](LICENSE).

**Why Apache 2.0?** This module uses Apache 2.0 to provide maximum flexibility for integration. Modules that connect via REST API are not affected by this license, allowing for easier commercial and open-source integration.

## Quick Start

### Prerequisites

- Python 3.11+
- Redis (for job queue)
- Access to Orion-LD Context Broker

### Local Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Copy environment template
cp ../env.example .env
# Edit .env with your configuration

# Run the service
uvicorn app.main:app --reload --port 8000
```

### Docker Development

```bash
# Build image
docker build -f backend/Dockerfile -t intelligence-backend:dev ./backend

# Run container
docker run -p 8000:8000 \
  -e REDIS_HOST=host.docker.internal \
  -e ORION_URL=http://host.docker.internal:1026 \
  intelligence-backend:dev
```

## Architecture

This is a **completely independent module** with:
- ✅ **Zero dependencies** on Core services code
- ✅ **Standalone Docker image** optimized for Data Science workloads
- ✅ **REST API** for triggering analysis and predictions
- ✅ **Redis-based job queue** for async processing
- ✅ **Orion-LD integration** for writing Prediction entities (NGSI-LD standard)

## Communication Contract

### Between Core and Intelligence Module

**Communication Channels:**

1. **Core → Module**: 
   - REST API: `POST /api/intelligence/analyze`
   - REST API: `POST /api/intelligence/predict`
   - Webhooks: `POST /api/intelligence/webhook/n8n`

2. **Module → Core**:
   - **ONLY** through Orion-LD: Module writes `Prediction` entities
   - Core reads these entities from Orion-LD (no direct API calls)

**Strict Separation:**
- ❌ No shared code libraries
- ❌ No imports from Core
- ✅ Pure REST API + Orion-LD contract
- ✅ Multi-tenant via `X-Tenant-ID` header

## Setup

### Prerequisites

- Python 3.11+
- Redis (for job queue)
- Access to Orion-LD Context Broker

### Installation

```bash
pip install -r requirements.txt
```

### Environment Variables

```bash
# Redis Configuration
REDIS_HOST=redis-service
REDIS_PORT=6379
REDIS_PASSWORD=<password>

# Orion-LD Configuration
ORION_URL=http://orion-ld-service:1026
CONTEXT_URL=https://nekazari.artotxiki.com/ngsi-ld-context.json

# Service Configuration
LOG_LEVEL=INFO
```

## Development

```bash
# Run locally
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

## Docker Build

```bash
docker build -t nekazari-module-intelligence:latest .
```

## API Endpoints

### Health Check
```
GET /health
```

### Trigger Analysis
```
POST /api/intelligence/analyze
Content-Type: application/json
X-Tenant-ID: <tenant_id>

{
  "entity_id": "urn:ngsi-ld:AgriSensor:sensor-123",
  "attribute": "temperature",
  "historical_data": [
    {"timestamp": "2024-01-15T10:00:00Z", "value": 20.5},
    {"timestamp": "2024-01-15T11:00:00Z", "value": 22.1}
  ],
  "prediction_horizon": 24,
  "plugin": "simple_predictor"
}
```

### Trigger Prediction (writes to Orion-LD)
```
POST /api/intelligence/predict
Content-Type: application/json
X-Tenant-ID: <tenant_id>

{
  "entity_id": "urn:ngsi-ld:AgriSensor:sensor-123",
  "attribute": "temperature",
  "historical_data": [...],
  "prediction_horizon": 24
}
```

### Get Job Status
```
GET /api/intelligence/jobs/{job_id}
```

### Webhook for n8n
```
POST /api/intelligence/webhook/n8n
Content-Type: application/json
X-Tenant-ID: <tenant_id>

{
  "entity_id": "urn:ngsi-ld:AgriSensor:sensor-123",
  "attribute": "temperature",
  "analysis_type": "predict",
  "data": {...}
}
```

## Plugins

Plugins implement the `IntelligencePlugin` interface. Current plugins:

- **simple_predictor**: Basic linear extrapolation (placeholder for ML)

To add ML plugins, uncomment data science libraries in `requirements.txt` and implement new plugins in `intelligence_service/plugins/`.

## Kubernetes Deployment

See `k8s/` directory for deployment manifests. The module runs as a standalone service with its own namespace or selectors.

## Migration Notes

This module was extracted from `services/intelligence-service/` to maintain strict separation from Core services. All dependencies on `common/` have been removed and replaced with standalone implementations.

