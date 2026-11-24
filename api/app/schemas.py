from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    display_name: str = Field(min_length=1, max_length=50)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    display_name: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RecipeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    servings: int = Field(ge=1)
    total_minutes: int | None = Field(default=None, ge=1, le=1440)


class RecipeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    title: str
    description: str | None
    servings: int
    total_minutes: int | None
    created_at: datetime
