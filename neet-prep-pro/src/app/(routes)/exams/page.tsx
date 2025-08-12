export default function ExamsPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Monthly Model Exams</h2>
      <p className="text-gray-600">Full-length practice at the end of each month.</p>
      <ul className="space-y-2 text-sm">
        <li className="rounded border p-4">June Model Exam</li>
        <li className="rounded border p-4">July Model Exam</li>
        <li className="rounded border p-4">August Model Exam</li>
      </ul>
    </div>
  );
}