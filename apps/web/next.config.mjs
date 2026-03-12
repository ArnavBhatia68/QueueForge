/** @type {import('next').NextConfig} */
const nextConfig = {
  // Prevent Next.js 308 redirects from modifying trailing-slash URLs on page routes
  skipTrailingSlashRedirect: true,
  async rewrites() {
    const apiBase = process.env.NEXT_PUBLIC_API_URL
      ? process.env.NEXT_PUBLIC_API_URL
      : 'http://127.0.0.1:8001/api/v1';

    return [
      // Handle URLs that already have a trailing slash — forward them directly
      // so FastAPI never needs to 307-redirect (which loses the Authorization header)
      {
        source: '/api/v1/:path*/',
        destination: `${apiBase}/:path*/`,
      },
      // Handle URLs without a trailing slash
      {
        source: '/api/v1/:path*',
        destination: `${apiBase}/:path*`,
      },
    ]
  },
}

export default nextConfig
