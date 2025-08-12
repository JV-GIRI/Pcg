import { NextResponse } from 'next/server';
import prisma from '@/lib/prisma';

export async function POST() {
  try {
    const chapters = await Promise.all([
      prisma.chapter.upsert({
        where: { id: 'phy-kinematics' },
        update: {},
        create: { id: 'phy-kinematics', subject: 'PHYSICS', title: 'Kinematics' },
      }),
      prisma.chapter.upsert({
        where: { id: 'chem-bonding' },
        update: {},
        create: { id: 'chem-bonding', subject: 'CHEMISTRY', title: 'Chemical Bonding' },
      }),
      prisma.chapter.upsert({
        where: { id: 'bio-cell' },
        update: {},
        create: { id: 'bio-cell', subject: 'BIOLOGY', title: 'Cell Structure' },
      }),
    ]);

    await prisma.lesson.upsert({
      where: { id: 'lesson-kinematics-1' },
      update: {},
      create: { id: 'lesson-kinematics-1', chapterId: 'phy-kinematics', title: 'Displacement and Velocity' },
    });

    await prisma.question.upsert({
      where: { id: 'q-kin-1' },
      update: {},
      create: {
        id: 'q-kin-1',
        chapterId: 'phy-kinematics',
        text: 'A particle moves with constant velocity of 5 m/s. What is the displacement after 4 s?',
        difficulty: 1,
        options: {
          create: [
            { idx: 0, text: '10 m', isCorrect: false },
            { idx: 1, text: '15 m', isCorrect: false },
            { idx: 2, text: '20 m', isCorrect: true },
            { idx: 3, text: '25 m', isCorrect: false },
          ],
        },
      },
    });

    return NextResponse.json({ ok: true, chaptersCount: chapters.length });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ ok: false, error: 'Seed failed' }, { status: 500 });
  }
}