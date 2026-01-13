from fastapi import FastAPI

app = FastAPI(title="Fin Analytics (Snowflake)")

@app.get("/health")
async def health():
    return {"status": "ok"}
