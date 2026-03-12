'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardLayout } from '@/components/dashboard-layout';
import { useAuthStore } from '@/hooks/use-auth';
import { api } from '@/lib/api';
import { User } from '@/types';

export default function Layout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { isAuthenticated, setAuth, setUser } = useAuthStore();
  const [isVerifying, setIsVerifying] = useState(true);

  useEffect(() => {
    const verifyAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) throw new Error('No token');
        
        const { data } = await api.get<User>('/auth/me');
        setUser(data);
        setAuth(true);
      } catch (error) {
        setAuth(false);
        router.push('/login');
      } finally {
        setIsVerifying(false);
      }
    };

    if (!isAuthenticated) {
      verifyAuth();
    } else {
      setIsVerifying(false);
    }
  }, [isAuthenticated, router, setAuth, setUser]);

  if (isVerifying) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return <DashboardLayout>{children}</DashboardLayout>;
}
