from sqlalchemy.orm import Session

from app.database import engine


def get_db():
    """Provide one database session per request, closed afterward."""
    with Session(engine) as session:
        yield session
