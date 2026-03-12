/** @type {import('next').NextConfig} */
const nextConfig = {
  // Proxy API requests in development
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL 
          ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*` 
          : 'http://localhost:8000/api/v1/:path*',
      },
    ]
  },
}

export default nextConfig
