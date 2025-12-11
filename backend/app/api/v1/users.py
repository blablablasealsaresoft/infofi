"""User management endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserWalletCreate, UserWalletResponse
from app.core.security import get_current_user

router = APIRouter()


@router.get("/me/wallets", response_model=list[UserWalletResponse])
async def get_my_wallets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's wallets"""
    # Wallets are loaded via relationship
    return current_user.wallets

