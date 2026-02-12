from app.services import run_daily_job


if __name__ == "__main__":
    snapshot, brief, _ = run_daily_job()
    print(f"Saved snapshot total=${snapshot.total_usd}")
    print(f"Saved brief id={brief.id}")
