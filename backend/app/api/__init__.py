"""
Intelligence Module Backend - API Routes

Main API router that includes all endpoint definitions.
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field

from app.core.redis_client import redis_client
from app.core.job_queue import JobQueue, JobStatus
from app.core.worker import IntelligenceWorker

logger = logging.getLogger(__name__)

# Router setup
router = APIRouter(tags=["Intelligence"])

# Global instances
job_queue: Optional[JobQueue] = None
worker: Optional[IntelligenceWorker] = None
worker_task: Optional[asyncio.Task] = None


# =============================================================================
# Request/Response Models
# =============================================================================

class AnalyzeRequest(BaseModel):
    """Request model for analysis endpoint."""
    entity_id: str = Field(..., description="Entity ID to analyze")
    attribute: str = Field(..., description="Attribute name to predict")
    historical_data: list = Field(..., description="Historical data points")
    prediction_horizon: int = Field(24, ge=1, le=168, description="Prediction horizon in hours (1-168)")
    plugin: str = Field("simple_predictor", description="Plugin to use for analysis")
    priority: int = Field(0, description="Job priority (higher = more urgent)")


class PredictRequest(BaseModel):
    """Request model for prediction endpoint."""
    entity_id: str = Field(..., description="Entity ID to predict")
    attribute: str = Field(..., description="Attribute name to predict")
    historical_data: list = Field(..., description="Historical data points")
    prediction_horizon: int = Field(24, ge=1, le=168, description="Prediction horizon in hours")
    plugin: str = Field("simple_predictor", description="Plugin to use")
    priority: int = Field(0, description="Job priority")


class WebhookRequest(BaseModel):
    """Request model for n8n webhook endpoint."""
    entity_id: Optional[str] = None
    attribute: Optional[str] = None
    analysis_type: str = Field("predict", description="Type of analysis to run")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional data")


# =============================================================================
# Initialization
# =============================================================================

async def initialize_worker():
    """Initialize job queue and worker."""
    global job_queue, worker, worker_task
    
    if job_queue is None:
        job_queue = JobQueue(redis_client.client)
        worker = IntelligenceWorker(job_queue)
        worker_task = asyncio.create_task(worker.run())


def extract_tenant_id(authorization: Optional[str] = None, x_tenant_id: Optional[str] = Header(None)) -> str:
    """Extract tenant ID from headers."""
    if x_tenant_id:
        return x_tenant_id
    return "default"


# =============================================================================
# Routes
# =============================================================================

@router.on_event("startup")
async def startup_event():
    """Initialize worker on startup."""
    await initialize_worker()


@router.post("/analyze")
async def trigger_analysis(
    request: AnalyzeRequest,
    x_tenant_id: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
):
    """
    Trigger an analysis job.
    
    Returns immediately with a job ID. Use GET /jobs/{job_id} to check status.
    """
    if not job_queue:
        await initialize_worker()
    
    tenant_id = extract_tenant_id(authorization, x_tenant_id)
    
    job_data = {
        "entity_id": request.entity_id,
        "attribute": request.attribute,
        "historical_data": request.historical_data,
        "prediction_horizon": request.prediction_horizon,
        "plugin": request.plugin,
        "priority": request.priority
    }
    
    job_id = await job_queue.create_job("analyze", job_data, tenant_id)
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Analysis job created"
    }


@router.post("/predict")
async def trigger_prediction(
    request: PredictRequest,
    x_tenant_id: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
):
    """
    Trigger a prediction job and write results to Orion-LD.
    
    Returns immediately with a job ID. Results will be written as Prediction entities in Orion-LD.
    """
    if not job_queue:
        await initialize_worker()
    
    tenant_id = extract_tenant_id(authorization, x_tenant_id)
    
    job_data = {
        "entity_id": request.entity_id,
        "attribute": request.attribute,
        "historical_data": request.historical_data,
        "prediction_horizon": request.prediction_horizon,
        "plugin": request.plugin,
        "priority": request.priority
    }
    
    job_id = await job_queue.create_job("predict", job_data, tenant_id)
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Prediction job created. Results will be written to Orion-LD."
    }


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get job status by ID."""
    if not job_queue:
        raise HTTPException(status_code=503, detail="Service not ready")
    
    job = await job_queue.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "id": job["id"],
        "type": job["type"],
        "status": job["status"],
        "created_at": job["created_at"],
        "updated_at": job["updated_at"],
        "result": job.get("result"),
        "error": job.get("error")
    }


@router.delete("/jobs/{job_id}")
async def cancel_job(job_id: str):
    """Cancel a pending job."""
    if not job_queue:
        raise HTTPException(status_code=503, detail="Service not ready")
    
    success = await job_queue.cancel_job(job_id)
    if not success:
        raise HTTPException(status_code=400, detail="Job cannot be cancelled or not found")
    
    return {"message": "Job cancelled successfully"}


@router.post("/webhook/n8n")
async def n8n_webhook(
    request: WebhookRequest,
    x_tenant_id: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
):
    """
    Webhook endpoint for n8n integration.
    
    Accepts webhook calls from n8n workflows and triggers analysis jobs.
    """
    if not job_queue:
        await initialize_worker()
    
    tenant_id = extract_tenant_id(authorization, x_tenant_id)
    
    # Extract entity_id and attribute from request
    entity_id = request.entity_id or request.data.get("entity_id")
    attribute = request.attribute or request.data.get("attribute")
    
    if not entity_id or not attribute:
        raise HTTPException(status_code=400, detail="entity_id and attribute are required")
    
    # Prepare job data
    job_data = {
        "entity_id": entity_id,
        "attribute": attribute,
        "historical_data": request.data.get("historical_data", []),
        "prediction_horizon": request.data.get("prediction_horizon", 24),
        "plugin": request.data.get("plugin", "simple_predictor"),
        "priority": request.data.get("priority", 0),
        **request.data
    }
    
    job_id = await job_queue.create_job(request.analysis_type, job_data, tenant_id)
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": f"{request.analysis_type} job created from webhook"
    }


@router.get("/plugins")
async def list_plugins():
    """List available analysis plugins."""
    if not worker:
        await initialize_worker()
    
    plugins = [
        {
            "name": name,
            "description": "Analysis plugin"
        }
        for name in worker.plugins.keys()
    ]
    
    return {"plugins": plugins}


