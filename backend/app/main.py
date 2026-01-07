"""
Intelligence Module Backend - FastAPI Application

Main entry point for the Intelligence Module backend service.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api import router as api_router
from app.core.redis_client import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events."""
    # Startup
    settings = get_settings()
    print(f"🚀 {settings.app_name} v{settings.app_version} starting...")
    print(f"   API Prefix: {settings.api_prefix}")
    print(f"   Redis: {settings.redis_host}:{settings.redis_port}")
    print(f"   Orion-LD: {settings.orion_url}")
    
    # Connect Redis
    await redis_client.connect()
    
    yield
    
    # Shutdown
    print(f"👋 {settings.app_name} shutting down...")
    await redis_client.close()


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI/ML Intelligence Module - Analysis and Prediction Service for Nekazari Platform",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        lifespan=lifespan,
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check (at root for k8s probes)
    @app.get("/health")
    async def health_check():
        """Health check endpoint for Kubernetes probes."""
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version,
        }
    
    # Include API routes
    app.include_router(api_router, prefix=settings.api_prefix)
    
    return app


# Create application instance
app = create_app()


