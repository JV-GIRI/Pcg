import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    lessons: [
      { id: 'phy-kinematics-1', subject: 'PHYSICS', title: 'Kinematics I' },
      { id: 'chem-bonding-1', subject: 'CHEMISTRY', title: 'Chemical Bonding I' },
      { id: 'bio-cell-1', subject: 'BIOLOGY', title: 'Cell Structure I' },
    ],
  });
}