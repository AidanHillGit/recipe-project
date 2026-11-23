from fastapi import FastAPI, Response, status
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.database import engine
from app.routers import auth, recipes


app = FastAPI(title="Recipe API")

app.include_router(auth.router)
app.include_router(auth.recipe)


@app.get("/health")
def health_check(response: Response) -> dict[str, str]:
    """Report that the API is running and the database is reachable."""
    try:
        with engine.connect() as connection:                                # open the connection
            connection.execute(text("SELECT 1"))                            # ask the database simplest question for health check
        return {"status": "ok", "database": "ok"}
    except OperationalError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "database": "unreachable"}
