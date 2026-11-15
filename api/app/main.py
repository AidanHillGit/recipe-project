from fastapi import FastAPI

app = FastAPI(title="Recipe API")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Report that the API is running."""
    return {"status": "ok"}
