'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Queue } from '@/types';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Layers } from 'lucide-react';

export default function QueuesPage() {
  const { data: queues, isLoading } = useQuery({
    queryKey: ['queues'],
    queryFn: async () => {
      const { data } = await api.get<Queue[]>('/queues/');
      return data;
    },
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Queues</h2>
        <p className="text-muted-foreground">
          View all configured queues in the platform.
        </p>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center space-x-2">
            <Layers className="h-5 w-5 text-muted-foreground" />
            <CardTitle>Configured Queues</CardTitle>
          </div>
          <CardDescription>
            Named queues that workers can consume jobs from.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Queue Name</TableHead>
                <TableHead>Description</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell colSpan={3} className="text-center py-4 text-muted-foreground">
                    Loading queues...
                  </TableCell>
                </TableRow>
              ) : queues?.map((q) => (
                <TableRow key={q.id}>
                  <TableCell className="font-semibold font-mono">{q.name}</TableCell>
                  <TableCell className="text-muted-foreground">{q.description || '-'}</TableCell>
                  <TableCell className="text-right">
                    <span className="text-sm text-primary cursor-pointer hover:underline">
                      View Jobs
                    </span>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
