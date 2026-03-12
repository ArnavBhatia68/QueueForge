from fastapi import APIRouter
from api.v1 import auth, queues, jobs, analytics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(queues.router, prefix="/queues", tags=["queues"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
