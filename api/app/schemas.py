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
