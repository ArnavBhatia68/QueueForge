from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from core.database import get_db
from models import Queue, User
from schemas import QueueCreate, QueueResponse
from api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=QueueResponse)
async def create_queue(
    queue_in: QueueCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Queue).where(Queue.name == queue_in.name)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Queue with this name already exists")
    
    queue = Queue(name=queue_in.name, description=queue_in.description)
    db.add(queue)
    await db.commit()
    await db.refresh(queue)
    return queue

@router.get("/", response_model=List[QueueResponse])
async def list_queues(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Queue)
    result = await db.execute(stmt)
    return result.scalars().all()
