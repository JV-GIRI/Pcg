import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'NEET Prep Pro',
  description: 'Daily lessons, mock tests, model exams, and adaptive learning for NEET.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen bg-white text-gray-900`}>
        <header className="border-b bg-white/70 backdrop-blur">
          <nav className="mx-auto max-w-7xl px-6 py-4 flex items-center justify-between">
            <Link href="/" className="text-xl font-semibold text-brand-700">NEET Prep Pro</Link>
            <div className="flex gap-4 text-sm">
              <Link href="/lessons" className="hover:text-brand-600">Lessons</Link>
              <Link href="/tests" className="hover:text-brand-600">Mock Tests</Link>
              <Link href="/exams" className="hover:text-brand-600">Model Exams</Link>
              <Link href="/analytics" className="hover:text-brand-600">Analytics</Link>
              <Link href="/progress" className="hover:text-brand-600">Progress</Link>
              <Link href="/papers" className="hover:text-brand-600">Old Papers</Link>
              <Link href="/aids" className="hover:text-brand-600">Aids</Link>
            </div>
          </nav>
        </header>
        <main className="mx-auto max-w-7xl px-6 py-8">{children}</main>
      </body>
    </html>
  );
}