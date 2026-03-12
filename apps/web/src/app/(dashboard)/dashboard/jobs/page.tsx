import { Metadata } from 'next';
import { JobsTable } from '@/components/dashboard/jobs-table';

export const metadata: Metadata = {
  title: 'Jobs | QueueForge',
  description: 'Manage and monitor background jobs',
};

export default function JobsPage() {
  return (
    <div className="space-y-6 flex flex-col h-full">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Jobs</h2>
        <p className="text-muted-foreground">
          Monitor execution status, inspect logs, and retry failures.
        </p>
      </div>
      
      <JobsTable />
    </div>
  );
}
