import { Metadata } from 'next';
import { OverviewCards } from '@/components/dashboard/overview-cards';

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
      
      {/* 
        We could add charts here via Recharts, 
        but leaving them out initially for speed 
      */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <div className="col-span-4 border rounded-xl p-6 bg-card flex items-center justify-center text-muted-foreground min-h-[300px]">
          [Analytics Chart Placeholder]
        </div>
        <div className="col-span-3 border rounded-xl p-6 bg-card flex items-center justify-center text-muted-foreground min-h-[300px]">
          [Recent Activity Log]
        </div>
      </div>
    </div>
  );
}
