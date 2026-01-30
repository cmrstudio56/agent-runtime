from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import task_execute, task_status

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("agent-runtime")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Application starting (local mode)")
    yield
    logger.info("🛑 Application shutting down")


app = FastAPI(
    title="Agent Runtime (Local)",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_execute.router, prefix="/task", tags=["tasks"])
app.include_router(task_status.router, prefix="/task", tags=["tasks"])


@app.get("/")
async def root():
    return {
        "service": "agent-runtime",
        "mode": "local",
        "status": "ok",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
