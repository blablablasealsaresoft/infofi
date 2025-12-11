"""User schemas"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    password: Optional[str] = Field(None, min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class WalletLogin(BaseModel):
    wallet_address: str = Field(..., regex=r"^0x[a-fA-F0-9]{40}$")
    signature: str
    message: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    email: Optional[str]
    username: str
    subscription_tier: str
    subscription_expires_at: Optional[datetime]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserWalletCreate(BaseModel):
    wallet_address: str = Field(..., regex=r"^0x[a-fA-F0-9]{40}$")
    chain: str = "ethereum"
    signature: str
    message: str


class UserWalletResponse(BaseModel):
    id: int
    wallet_address: str
    chain: str
    is_primary: bool
    verified_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

