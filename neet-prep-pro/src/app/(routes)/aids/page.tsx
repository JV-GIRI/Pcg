export default function AidsPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Interactive Teaching Aids</h2>
      <p className="text-gray-600">Quizzes, flashcards, and animations to reinforce concepts.</p>
      <div className="grid md:grid-cols-3 gap-3 text-sm">
        <div className="rounded border p-4">Quick Quiz</div>
        <div className="rounded border p-4">Flashcards</div>
        <div className="rounded border p-4">Concept Animations</div>
      </div>
    </div>
  );
}