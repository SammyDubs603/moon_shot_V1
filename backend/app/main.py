from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import db
from app.config import get_settings
from app.models import OverviewResponse, RunDailyResponse
from app.services import run_daily_job


app = FastAPI(title="Coinbase Portfolio Trade Recommender")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    password: str


def require_auth(session: Annotated[str | None, Cookie()] = None) -> None:
    if session != "ok":
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.on_event("startup")
def startup() -> None:
    db.migrate()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.post("/api/login")
def login(payload: LoginRequest, response: Response) -> dict[str, str]:
    if payload.password != get_settings().app_password:
        raise HTTPException(status_code=401, detail="Invalid password")
    response.set_cookie("session", "ok", httponly=True, samesite="lax")
    return {"status": "ok"}


@app.get("/api/overview", response_model=OverviewResponse)
def overview(_: None = Depends(require_auth)) -> OverviewResponse:
    return OverviewResponse(snapshot=db.latest_snapshot(), brief=db.latest_brief(), ai_summary=db.latest_ai_summary())


@app.get("/api/snapshots")
def snapshots(limit: int = 60, _: None = Depends(require_auth)):
    return {"items": db.list_snapshots(limit)}


@app.get("/api/briefs")
def briefs(limit: int = 20, _: None = Depends(require_auth)):
    return {"items": db.list_briefs(limit)}


@app.post("/api/run-daily", response_model=RunDailyResponse)
def run_daily(_: None = Depends(require_auth)) -> RunDailyResponse:
    snapshot, brief, ai_summary = run_daily_job()
    return RunDailyResponse(status="ok", snapshot=snapshot, brief=brief, ai_summary=ai_summary)
