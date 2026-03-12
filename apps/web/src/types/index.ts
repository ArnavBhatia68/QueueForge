export type JobStatus = 'queued' | 'running' | 'succeeded' | 'failed' | 'retrying' | 'cancelled';

export interface User {
  id: number;
  email: string;
}

export interface Queue {
  id: number;
  name: string;
  description: string | null;
}

export interface Job {
  id: number;
  queue_name: string;
  type: string;
  priority: number;
  status: JobStatus;
  attempts: number;
  max_retries: number;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
  result: string | null;
  worker_id: string | null;
  payload: string | null;
}

export interface JobLog {
  id: number;
  job_id: number;
  message: string;
  timestamp: string;
  level: string;
}

export interface JobDetail extends Job {
  logs: JobLog[];
}

export interface AnalyticsOverview {
  total_jobs: number;
  running_jobs: number;
  failed_jobs: number;
  success_rate: number;
  avg_processing_time_ms: number;
}
