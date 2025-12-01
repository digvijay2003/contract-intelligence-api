"""Main FastAPI application for Contract Intelligence API"""
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import time

from app.core.config import settings
from app.core.logging import logger
from app.db.session import get_db
from app.db.models import Base, Document
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contract Intelligence API",
    description="RAG-powered contract analysis and risk detection",
    version="1.0.0"
)


metrics = {
    "total_requests": 0,
    "requests_by_endpoint": {},
    "avg_latency_ms": {},
}


def track_metrics(endpoint: str, latency_ms: float):
    """Track basic metrics"""
    metrics["total_requests"] += 1
    metrics["requests_by_endpoint"][endpoint] = metrics["requests_by_endpoint"].get(endpoint, 0) + 1
    
    if endpoint not in metrics["avg_latency_ms"]:
        metrics["avg_latency_ms"][endpoint] = []
    metrics["avg_latency_ms"][endpoint].append(latency_ms)


@app.get("/")
async def root():
    return {
        "message": "Contract Intelligence API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/healthz")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": int(time.time())
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.get("/metrics")
async def get_metrics():
    """Get basic API metrics"""
    avg_latencies = {}
    for endpoint, latencies in metrics["avg_latency_ms"].items():
        if latencies:
            avg_latencies[endpoint] = sum(latencies) / len(latencies)
    
    return {
        "total_requests": metrics["total_requests"],
        "requests_by_endpoint": metrics["requests_by_endpoint"],
        "avg_latency_ms": avg_latencies
    }


import asyncio

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Contract Intelligence API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)