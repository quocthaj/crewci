import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from orchestrator.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_path = os.getenv("CREWCI_DB_PATH", "data/crewci.db")
    init_db(db_path).close()
    yield


app = FastAPI(title="CrewCI", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
