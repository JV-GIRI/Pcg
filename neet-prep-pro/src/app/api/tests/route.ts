import { NextResponse } from 'next/server';

export async function GET() {
  const tests = [
    { id: 'quick-45', title: 'Quick 45', type: 'mock', questions: 45 },
    { id: 'full-neet', title: 'Full NEET', type: 'mock', questions: 180 },
  ];
  return NextResponse.json({ tests });
}