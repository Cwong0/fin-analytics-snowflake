from fastapi import FastAPI
import os
import platform
import time

START_TIME = time.time()

app = FastAPI(title="Fin Analytics (Snowflake)")

@app.get("/health")
async def health():
    """Combined health endpoint (good for local/dev)."""
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "env": os.getenv("APP_ENV", "dev"),
        "python": platform.python_version(),
        "platform": platform.platform(),
    }

@app.get("/health/live")
async def live():
    """Liveness: process is up."""
    return {"status": "ok"}

@app.get("/health/ready")
async def ready():
    """Readiness: dependencies/config are present (Snowflake check later)."""
    required = ["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER", "SNOWFLAKE_DATABASE"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        return {"status": "not_ready", "missing_env": missing}
    return {"status": "ready"}
