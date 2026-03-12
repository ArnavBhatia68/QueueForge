import { Metadata } from 'next';
import { OverviewCards } from '@/components/dashboard/overview-cards';
import { JobStatusChart } from '@/components/charts/JobStatusChart';
import { RecentActivity } from '@/components/dashboard/RecentActivity';

export const metadata: Metadata = {
  title: 'Dashboard | QueueForge',
  description: 'QueueForge platform overview and analytics',
};

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Overview</h2>
        <p className="text-muted-foreground">
          Platform performance and queue metrics.
        </p>
      </div>

      <OverviewCards />

      <div className="grid gap-4 md:grid-cols-7">
        <JobStatusChart />
        <RecentActivity />
      </div>
    </div>
  );
}
