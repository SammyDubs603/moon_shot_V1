'use client';

import { useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export function LoginGate({ onAuthed }: { onAuthed: () => void }) {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  return (
    <div className="card max-w-md">
      <h2 className="mb-2 text-lg font-semibold">Private Dashboard Login</h2>
      <input
        className="w-full rounded-lg border border-border bg-transparent p-2"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter dashboard password"
      />
      <button
        className="mt-3 rounded-xl bg-blue-600 px-4 py-2"
        onClick={async () => {
          setError('');
          const res = await fetch(`${API}/api/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ password })
          });
          if (!res.ok) {
            setError('Invalid password');
            return;
          }
          onAuthed();
        }}
      >Login</button>
      {error && <p className="mt-2 text-sm text-red-400">{error}</p>}
    </div>
  );
}
