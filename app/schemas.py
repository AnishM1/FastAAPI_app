from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Any, List

class APIResponse(BaseModel):
    message: str
    data: Optional[Any] = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: bool = True

class Login(BaseModel):
    username_or_email: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: Optional[str] = None
    bio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str

    model_config = ConfigDict(from_attributes=True)
