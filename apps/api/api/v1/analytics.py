from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from core.database import get_db
from models import Job, JobStatus, Queue, User
from schemas import AnalyticsOverview
from api.deps import get_current_user

router = APIRouter()

@router.get("/overview", response_model=AnalyticsOverview)
async def get_overview_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Total jobs
    total_result = await db.execute(select(func.count(Job.id)))
    total_jobs = total_result.scalar() or 0

    # Running jobs
    running_result = await db.execute(select(func.count(Job.id)).where(Job.status == JobStatus.RUNNING))
    running_jobs = running_result.scalar() or 0

    # Failed jobs
    failed_result = await db.execute(select(func.count(Job.id)).where(Job.status == JobStatus.FAILED))
    failed_jobs = failed_result.scalar() or 0

    # Success rate
    success_result = await db.execute(select(func.count(Job.id)).where(Job.status == JobStatus.SUCCEEDED))
    success_jobs = success_result.scalar() or 0
    
    success_rate = 0.0
    if total_jobs > 0:
        # success rate of completed jobs
        completed = success_jobs + failed_jobs
        if completed > 0:
            success_rate = (success_jobs / completed) * 100.0

    # Avg processing time (started_at to completed_at where not null)
    # Using python processing for simplicity since SQlite/Postgres differences in interval handling can be complex
    stmt = select(Job.started_at, Job.completed_at).where(
        Job.status == JobStatus.SUCCEEDED,
        Job.started_at.isnot(None),
        Job.completed_at.isnot(None)
    )
    times_result = await db.execute(stmt)
    times = times_result.all()
    
    avg_processing_time_ms = 0.0
    if times:
        total_ms = sum(
            (t.completed_at - t.started_at).total_seconds() * 1000 for t in times
        )
        avg_processing_time_ms = total_ms / len(times)

    return AnalyticsOverview(
        total_jobs=total_jobs,
        running_jobs=running_jobs,
        failed_jobs=failed_jobs,
        success_rate=round(success_rate, 2),
        avg_processing_time_ms=round(avg_processing_time_ms, 2)
    )
