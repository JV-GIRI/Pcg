# NEET Prep Pro (Next.js)

A comprehensive NEET preparation platform with daily lessons, mock tests, monthly model exams, score analytics, and adaptive learning.

## Tech
- Next.js (App Router, TypeScript)
- Tailwind CSS
- Prisma + SQLite (local dev)

## Setup
1. Copy env:
   ```bash
   cp .env.example .env
   ```
2. Install deps:
   ```bash
   npm install
   ```
3. Initialize DB:
   ```bash
   npx prisma generate
   npx prisma migrate dev --name init
   ```
4. Run dev server:
   ```bash
   npm run dev
   ```

## Scripts
- `npm run dev` — start dev server
- `npm run build` — production build
- `npm start` — start production server
- `npm run prisma:generate` — generate Prisma client
- `npm run prisma:migrate` — run dev migration

## Structure
- `src/app` — routes and layouts
- `src/components` — UI components
- `src/lib` — utilities (e.g., Prisma client)
- `prisma/schema.prisma` — DB schema

## Notes
- API endpoints currently return mock data; wire to Prisma as needed.