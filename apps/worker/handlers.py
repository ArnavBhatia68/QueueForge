import asyncio
import json
import random

async def send_email(payload: dict) -> dict:
    """Mock sending an email"""
    await asyncio.sleep(random.uniform(1.0, 3.0))
    if random.random() < 0.1:
        raise Exception("SMTP Connection Timeout")
    return {"message": "Email sent successfully", "to": payload.get("email", "unknown@example.com")}

async def generate_report(payload: dict) -> dict:
    """Mock report generation"""
    await asyncio.sleep(random.uniform(3.0, 7.0))
    return {"report_url": "https://queueforge.local/reports/req_123.pdf", "pages": random.randint(1, 50)}

async def process_csv(payload: dict) -> dict:
    """Mock CSV processing"""
    await asyncio.sleep(random.uniform(2.0, 5.0))
    if random.random() < 0.2:
        raise ValueError("Malformed CSV line 42")
    return {"rows_processed": random.randint(100, 10000)}

async def simulate_ml_task(payload: dict) -> dict:
    """Mock ML task processing"""
    await asyncio.sleep(random.uniform(5.0, 12.0))
    return {"confidence": random.uniform(0.7, 0.99), "label": "fraud"}

HANDLERS = {
    "send_email": send_email,
    "generate_report": generate_report,
    "process_csv": process_csv,
    "simulate_ml_task": simulate_ml_task,
}
