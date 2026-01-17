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

from fin_analytics.models.prices import PriceIn

@app.post("/ingest/prices")
async def ingest_prices(payload: list[PriceIn]):
    # Later: load to Snowflake stage and MERGE; for now: validate + summarize
    return {
        "received": len(payload),
        "first": payload[0].model_dump() if payload else None
    }

from fin_analytics.snowflake.client import missing_env, ping

@app.get("/health/ready")
async def ready():
    missing = missing_env()
    if missing:
        return {"status": "not_ready", "missing_env": missing}

    try:
        ok = ping()
        return {"status": "ready" if ok else "not_ready"}
    except Exception as e:
        return {"status": "not_ready", "error": str(e)}


from fin_analytics.snowflake.client import missing_env as sf_missing_env, ping as sf_ping

@app.get("/health/snowflake")
async def health_snowflake():
    missing = sf_missing_env()
    if missing:
        return {"status": "not_configured", "missing_env": missing}
    ok = sf_ping()
    return {"status": "ok" if ok else "error"}
