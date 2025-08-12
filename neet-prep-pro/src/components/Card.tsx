import { PropsWithChildren } from 'react';

export function Card({ children }: PropsWithChildren) {
  return <div className="rounded-lg border bg-white p-5 shadow-sm">{children}</div>;
}