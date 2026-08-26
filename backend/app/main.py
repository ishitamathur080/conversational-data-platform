"""
FastAPI Application Factory and Configuration
PHASE 1: Core Infrastructure & Database Layer
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from app.database.connection import engine, Base
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.tenant_middleware import TenantMiddleware
from app.utils.logger import logger

# Import all models to ensure they are registered with SQLAlchemy
from app.models import company, tenant, user, database, audit

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events
    """
    # Startup
    logger.info("Starting Conversational Data Platform...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")
    yield
    # Shutdown
    logger.info("Shutting down Conversational Data Platform...")

def create_app() -> FastAPI:
    """
    Application Factory - Creates and configures the FastAPI application
    """
    app = FastAPI(
        title="Conversational Data Platform",
        description="A secure multi-tenant conversational data platform",
        version="1.0.0",
        lifespan=lifespan
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted Host Middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost").split(",")
    )

    # Custom Middlewares
    app.add_middleware(TenantMiddleware)
    app.add_middleware(AuthMiddleware)

    # Include routers
    from app.api.routes import auth, companies, tenants, databases, schemas, queries, results, admin
    
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(companies.router, prefix="/api/v1/companies", tags=["Companies"])
    app.include_router(tenants.router, prefix="/api/v1/tenants", tags=["Tenants"])
    app.include_router(databases.router, prefix="/api/v1/databases", tags=["Databases"])
    app.include_router(schemas.router, prefix="/api/v1/schemas", tags=["Schemas"])
    app.include_router(queries.router, prefix="/api/v1/queries", tags=["Queries"])
    app.include_router(results.router, prefix="/api/v1/results", tags=["Results"])
    app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "conversational-data-platform"}

    return app

app = create_app()
