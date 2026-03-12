'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardLayout } from '@/components/dashboard-layout';
import { useAuthStore } from '@/hooks/use-auth';
import { api } from '@/lib/api';
import { User } from '@/types';

export default function Layout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { isAuthenticated, setAuth, setUser, logout } = useAuthStore();
  const [isVerifying, setIsVerifying] = useState(!isAuthenticated);

  useEffect(() => {
    // Always re-validate the JWT with the server on mount (security check).
    // Because Zustand persist has already set isAuthenticated=true from the
    // previous session, we don't redirect until we know the token is actually bad.
    const verifyAuth = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        logout();
        router.replace('/login');
        return;
      }

      try {
        const { data } = await api.get<User>('/auth/me');
        setUser(data);
        setAuth(true);
      } catch {
        logout();
        router.replace('/login');
      } finally {
        setIsVerifying(false);
      }
    };

    verifyAuth();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (isVerifying) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return <DashboardLayout>{children}</DashboardLayout>;
}
