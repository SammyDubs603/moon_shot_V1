import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        bg: '#0f172a',
        card: '#111827',
        border: '#1f2937',
        text: '#e5e7eb',
        muted: '#94a3b8'
      }
    }
  },
  plugins: []
};

export default config;
