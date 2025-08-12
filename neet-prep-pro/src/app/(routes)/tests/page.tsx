export default function TestsPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Mock Tests</h2>
      <p className="text-gray-600">Take timed tests that mimic NEET format.</p>
      <div className="grid md:grid-cols-2 gap-3">
        <div className="rounded border p-4">
          <div className="font-medium">Quick 45</div>
          <div className="text-sm text-gray-600">45 questions · 45 minutes</div>
        </div>
        <div className="rounded border p-4">
          <div className="font-medium">Full NEET</div>
          <div className="text-sm text-gray-600">180 questions · 200 minutes</div>
        </div>
      </div>
    </div>
  );
}