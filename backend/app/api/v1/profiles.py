"""Profile endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.profile import PlatformProfile
from app.core.security import get_current_user

router = APIRouter()


@router.get("/me")
async def get_my_profiles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's platform profiles"""
    
    # Get all wallets for this user
    wallet_ids = [w.id for w in current_user.wallets]
    
    # Get all profiles linked to those wallets
    result = await db.execute(
        select(PlatformProfile).where(
            PlatformProfile.user_wallet_id.in_(wallet_ids)
        )
    )
    profiles = result.scalars().all()
    
    return profiles

