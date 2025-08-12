export default function AnalyticsPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Score Analysis</h2>
      <p className="text-gray-600">Personalized feedback after each test.</p>
      <div className="grid md:grid-cols-3 gap-3 text-sm">
        <div className="rounded border p-4">Strengths: Biology</div>
        <div className="rounded border p-4">Weaknesses: Physics Mechanics</div>
        <div className="rounded border p-4">Focus: Chemical Kinetics</div>
      </div>
    </div>
  );
}