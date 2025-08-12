export default function PapersPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Old Question Papers</h2>
      <p className="text-gray-600">Practice with previous years' NEET papers and solutions.</p>
      <ul className="space-y-2 text-sm">
        <li className="rounded border p-4">NEET 2023 — Paper + Solutions</li>
        <li className="rounded border p-4">NEET 2022 — Paper + Solutions</li>
        <li className="rounded border p-4">NEET 2021 — Paper + Solutions</li>
      </ul>
    </div>
  );
}