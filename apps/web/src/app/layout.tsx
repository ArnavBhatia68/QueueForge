import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Providers from "@/components/providers";
import { Toaster } from "@/components/ui/sonner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "QueueForge | Distributed Job Platform",
  description: "A production-grade job queue processing and analytics platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-background text-foreground antialiased min-h-screen flex flex-col`}>
        <Providers>
          {children}
        </Providers>
        <Toaster position="top-right" />
      </body>
    </html>
  );
}
