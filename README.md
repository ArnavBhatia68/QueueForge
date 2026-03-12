# QueueForge

QueueForge is a production-grade, distributed background job processing platform with a polished, real-time administrative dashboard.

Built as a comprehensive portfolio project, QueueForge demonstrates a modern approach to asynchronous architectural patterns. It features an API-driven control plane, robust Python workers, Redis message passing, and a sleek Next.js (App Router) interface. 

![QueueForge Architecture](./docs/architecture.png)

## Why It Matters
Modern SaaS applications rely heavily on background processing to keep web requests fast and reliable. QueueForge implements common patterns seen in production platforms like Celery, BullMQ, or Sidekiq but consolidates the control plane and visibility into an easy-to-deploy package with a premium user experience.

## Architecture

```mermaid
graph TD
    A[Web Client (Next.js)] -->|REST API (FastAPI)| B(API Service)
    B -->|State / Logs| C[(PostgreSQL)]
    B -.->|Enqueue Job ID| D[(Redis Broker)]
    E[Worker Node (Python)] -.->|BLPOP| D
    E -->|Execute Handlers| F[Job Logic]
    E -->|Update Status| C
```

## Tech Stack
**Frontend (Web Dashboard)**
- Framework: Next.js 15 (App Router)
- Language: TypeScript
- UI/Styling: Tailwind CSS, shadcn/ui
- State & Data Fetching: Zustand, React Query `@tanstack/react-query`

**Backend (API & Worker)**
- Frameworks: FastAPI
- Database ORM: SQLAlchemy (Async), Alembic
- Language: Python 3.12
- Message Broker: Redis (`redis-py`)

**Infrastructure**
- Database: PostgreSQL
- Containerization: Docker, docker-compose
- CI: GitHub Actions

---

## Features
- **Job Lifecycle Management**: Enqueue, monitor, retry, or cancel jobs with full observability.
- **Real-Time Polished Dashboard**: Track overall system KPIs (success rates, current loads) via a Next.js frontend with dark mode support.
- **Robust Worker Architecture**: Python worker nodes asynchronously pull from Redis lists, execute defined handlers, and persist granular logs to PostgreSQL.
- **Multi-Queue Routing**: Prioritize tasks and route them to isolated named queues.
- **Resilience**: Auto-retries with configurable limits and exponential backoff mechanisms.

## Local Setup
Ensure you have Docker and Docker Compose installed.

### 1. Start Infrastructure
Start PostgreSQL and Redis in the background:
```bash
docker-compose up -d
```

### 2. Configure Environment
Copy `.env.example` to `.env` in the root folder.
```bash
cp .env.example .env
```

### 3. Setup Backend API
The FastAPI service handles the core REST layer and DB migrations.
```bash
cd apps/api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run migrations to build the tables
alembic upgrade head

# Seed demo queues, jobs, and a test user
python scripts/seed.py

# Start the API server on :8000
uvicorn main:app --reload
```

### 4. Start the Worker Service
The background worker consumes jobs from the queues.
Open a new terminal tab:
```bash
cd apps/worker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### 5. Launch the Web Dashboard
```bash
cd apps/web
npm install
npm run dev
```

Visit `http://localhost:3000` and sign in with:
**Email:** `demo@queueforge.io`
**Password:** `password`

## Deployment Guidelines
QueueForge is structurally ready for cloud deployments.
- **Web App**: Seamlessly deploys to [Vercel](https://vercel.com).
- **API & Worker**: Deployable via Dockerfiles to [Render](https://render.com) or [Railway](https://railway.app). Set standard horizontal scaling for the Worker instances based on queue depth.
- **Databases**: Use managed PostgreSQL (like [Neon](https://neon.tech)) and managed Redis (like [Upstash](https://upstash.com)).

## API Summary
The API follows standard REST principles and uses JWT authentication.
- `POST /api/v1/auth/login` - Obtain Access Token
- `GET /api/v1/jobs` - List jobs with optional status/queue filtering
- `POST /api/v1/jobs` - Enqueue a new execution
- `GET /api/v1/jobs/{id}` - Retrieve details and execution logs
- `POST /api/v1/jobs/{id}/retry` - Re-enqueue a failed job
- `POST /api/v1/jobs/{id}/cancel` - Abort a queued job
- `GET /api/v1/analytics/overview` - Fetch platform KPIs

## Future Enhancements
- CRON schedule triggers for recurring jobs.
- WebSocket streaming for dashboard updates (currenly uses smart polling).
- Complex DAG (Directed Acyclic Graph) workflow dependencies.
