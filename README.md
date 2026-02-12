# Coinbase Portfolio Trade Recommender (Private Dashboard)

Full-stack private dashboard with FastAPI + Next.js.

## Features
- Coinbase balances (Advanced Trade accounts endpoint) with demo fallback when keys are absent.
- Portfolio snapshot storage (SQLite): `portfolio_snapshots`, `trade_briefs`, `ai_summaries`.
- Deterministic BTC/ETH trade brief (trend + momentum + volatility/risk gate).
- OpenAI summary panel (explain deterministic output + changes since yesterday).
- Mobile-friendly dark UI with equity curve, holdings, and brief cards.
- Password-protected API session cookie.

## Project structure
- `backend/app/main.py` FastAPI API
- `backend/app/jobs/run_daily.py` cron entrypoint
- `frontend/app/*` dashboard pages

## Setup
1. Copy `.env.example` to `.env` and fill values.
2. Backend:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```
3. Frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Daily job
Manual/cron-friendly run:
```bash
cd backend
python -m app.jobs.run_daily
```

### Scheduler examples
- **Windows Task Scheduler**: create Basic Task -> daily trigger -> program `python` -> args `-m app.jobs.run_daily` -> start in `<repo>\\backend`.
- **Linux/macOS cron**:
  ```cron
  10 8 * * * cd /path/to/repo/backend && /path/to/python -m app.jobs.run_daily
  ```

Use UI **Run Daily** button (POST `/api/run-daily`) after login for on-demand refresh.

## API routes
- `GET /api/health`
- `POST /api/login`
- `GET /api/overview`
- `GET /api/snapshots?limit=...`
- `GET /api/briefs?limit=...`
- `POST /api/run-daily`

## Notes
- v1 is recommendation-only (no live trading execution).
- OpenAI is server-side only; keys are never exposed to browser.
