import type { NextRequest } from 'next/server';

export function middleware(_req: NextRequest) {
  // Placeholder for future auth or analytics
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};