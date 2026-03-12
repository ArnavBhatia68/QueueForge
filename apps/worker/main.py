import asyncio
import json
import logging
import traceback
from datetime import datetime
from sqlalchemy.future import select
import redis.asyncio as aioredis # type: ignore

from core.config import settings
from db.database import db_manager
from models.job import Job, JobLog, JobStatus
from handlers import HANDLERS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("worker")

class Worker:
    def __init__(self):
        self.redis = None
        self.queues = [q.strip() for q in settings.QUEUES_TO_WATCH.split(",")]
        self.running = False
        self.worker_id = settings.WORKER_ID

    async def start(self):
        logger.info(f"Starting Worker {self.worker_id}")
        self.redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        self.running = True

        queue_keys = [f"queue:{q}" for q in self.queues]
        logger.info(f"Watching queues: {queue_keys}")

        while self.running:
            try:
                # BLPOP blocks until an item is available in any of the queues
                result = await self.redis.blpop(queue_keys, timeout=settings.POLL_INTERVAL_SEC)
                if result:
                    queue_name, item = result
                    await self.process_job_msg(item)
            except asyncio.CancelledError:
                logger.info("Worker cancelled")
                break
            except Exception as e:
                logger.error(f"Error in poll loop: {e}")
                await asyncio.sleep(1)
        
        await self.redis.aclose() # type: ignore
        logger.info("Worker stopped")

    async def log_job(self, session, job_id, message, level="INFO"):
        session.add(JobLog(job_id=job_id, message=message, level=level))

    async def process_job_msg(self, msg_str: str):
        try:
            msg = json.loads(msg_str)
            job_id = msg.get("job_id")
            if not job_id:
                return
        except json.JSONDecodeError:
            logger.error(f"Failed to decode message: {msg_str}")
            return

        async with db_manager as session:
            # Fetch job
            stmt = select(Job).where(Job.id == job_id)
            result = await session.execute(stmt)
            job = result.scalars().first()

            if not job:
                logger.error(f"Job {job_id} not found in DB")
                return

            if job.status == JobStatus.CANCELLED:
                logger.info(f"Job {job_id} is cancelled, ignoring.")
                return 

            # Start job
            logger.info(f"Processing job {job_id} of type {job.type}")
            job.status = JobStatus.RUNNING
            job.attempts += 1
            job.started_at = datetime.utcnow()
            job.worker_id = self.worker_id
            
            await self.log_job(session, job.id, f"Job started on {self.worker_id} (Attempt {job.attempts})")
            await session.commit()
            
            # Execute
            success = False
            result_data = None
            error_msg = None
            
            try:
                handler_fn = HANDLERS.get(job.type)
                if not handler_fn:
                    raise ValueError(f"Unknown job type: {job.type}")
                    
                payload = json.loads(job.payload) if job.payload else {}
                result_data = await handler_fn(payload)
                success = True
            except Exception as e:
                logger.error(f"Job {job_id} failed: {e}")
                error_msg = str(e)
                traceback.print_exc()

            # Finish job
            job.completed_at = datetime.utcnow()
            
            if success:
                job.status = JobStatus.SUCCEEDED
                job.result = json.dumps(result_data)
                await self.log_job(session, job.id, "Job completed successfully")
            else:
                job.error_message = error_msg
                if job.attempts >= job.max_retries:
                    job.status = JobStatus.FAILED
                    await self.log_job(session, job.id, f"Job failed after {job.attempts} attempts: {error_msg}", level="ERROR")
                else:
                    job.status = JobStatus.RETRYING
                    await self.log_job(session, job.id, f"Job failed, scheduling retry: {error_msg}", level="WARNING")
                    # Re-enqueue
                    await self.redis.rpush(f"queue:{job.queue_name}", json.dumps({"job_id": job.id}))
                    job.status = JobStatus.QUEUED # Reset to queued for UI
            
            await session.commit()

if __name__ == "__main__":
    worker = Worker()
    try:
        asyncio.run(worker.start())
    except KeyboardInterrupt:
        logger.info("Shutting down worker...")
        worker.running = False
