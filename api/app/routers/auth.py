from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi import Depends, HTTPException, APIRouter, status


from app.deps import get_db
from app.models import User
from app.schemas import UserCreate, UserRead
from app.security import hash_password


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def register(user_in: UserCreate, db: Annotated[Session, Depends(get_db)]):
    """Create a new user account"""
    user = User(
        email=user_in.email,
        display_name=user_in.display_name,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    
    db.refresh(user)
    return user
