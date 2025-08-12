export default function HomePage() {
  return (
    <div className="space-y-8">
      <section className="rounded-lg border p-6 bg-white">
        <h1 className="text-2xl font-semibold text-gray-900">Welcome to NEET Prep Pro</h1>
        <p className="mt-2 text-gray-600">
          Daily lessons in Physics, Chemistry, and Biology. Practice with mock tests and monthly model exams. Get detailed analytics and adaptive recommendations to reach 650/720.
        </p>
      </section>

      <section className="grid md:grid-cols-3 gap-4">
        <a href="/lessons" className="rounded-lg border p-5 hover:border-brand-300">
          <h3 className="font-medium">Daily Lessons</h3>
          <p className="text-sm text-gray-600">New content every day across subjects.</p>
        </a>
        <a href="/tests" className="rounded-lg border p-5 hover:border-brand-300">
          <h3 className="font-medium">Mock Tests</h3>
          <p className="text-sm text-gray-600">Timed tests that mimic NEET format.</p>
        </a>
        <a href="/exams" className="rounded-lg border p-5 hover:border-brand-300">
          <h3 className="font-medium">Monthly Model Exams</h3>
          <p className="text-sm text-gray-600">Full-length practice every month.</p>
        </a>
      </section>

      <section className="grid md:grid-cols-3 gap-4">
        <a href="/analytics" className="rounded-lg border p-5 hover:border-brand-300">
          <h3 className="font-medium">Score Analysis</h3>
          <p className="text-sm text-gray-600">Understand strengths and gaps.</p>
        </a>
        <a href="/progress" className="rounded-lg border p-5 hover:border-brand-300">
          <h3 className="font-medium">Progress</h3>
          <p className="text-sm text-gray-600">Track improvement over time.</p>
        </a>
        <a href="/papers" className="rounded-lg border p-5 hover:border-brand-300">
          <h3 className="font-medium">Old Papers</h3>
          <p className="text-sm text-gray-600">Past exams with solutions.</p>
        </a>
      </section>
    </div>
  );
}