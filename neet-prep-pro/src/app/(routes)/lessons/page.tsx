export default function LessonsPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Daily Lessons</h2>
      <p className="text-gray-600">Browse lessons by subject and chapter.</p>
      <ul className="grid md:grid-cols-3 gap-3 text-sm">
        <li className="rounded border p-4">Physics — Kinematics</li>
        <li className="rounded border p-4">Chemistry — Chemical Bonding</li>
        <li className="rounded border p-4">Biology — Cell Structure</li>
      </ul>
    </div>
  );
}