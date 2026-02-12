import './globals.css';
import Link from 'next/link';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>
        <main className="mx-auto min-h-screen max-w-6xl p-4 md:p-6">
          <header className="mb-6 flex items-center justify-between">
            <h1 className="text-xl font-bold">Coinbase Portfolio Recommender</h1>
            <nav className="flex gap-3 text-sm text-muted">
              <Link href="/">Overview</Link>
              <Link href="/brief">Brief</Link>
              <Link href="/history">History</Link>
            </nav>
          </header>
          {children}
        </main>
      </body>
    </html>
  );
}
