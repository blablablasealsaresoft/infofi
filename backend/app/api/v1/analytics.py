"""Analytics endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from app.db.session import get_db
from app.models.user import User
from app.models.platform import Campaign
from app.models.profile import PlatformProfile
from app.core.security import get_current_user

router = APIRouter()


@router.get("/dashboard-stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard statistics"""
    
    # Total active campaigns
    campaign_count = await db.execute(
        select(func.count()).select_from(Campaign).where(Campaign.status == 'active')
    )
    total_campaigns = campaign_count.scalar()
    
    # User's average rank (if they have profiles)
    wallet_ids = [w.id for w in current_user.wallets]
    if wallet_ids:
        avg_rank_query = await db.execute(
            select(func.avg(PlatformProfile.global_rank)).where(
                PlatformProfile.user_wallet_id.in_(wallet_ids),
                PlatformProfile.global_rank.isnot(None)
            )
        )
        avg_rank = avg_rank_query.scalar() or 0
    else:
        avg_rank = 0
    
    return {
        "totalCampaigns": total_campaigns,
        "avgRank": int(avg_rank) if avg_rank else None,
        "shillScore": 0,  # Placeholder
        "estimatedValue": 0  # Placeholder
    }


@router.get("/leaderboard/global")
async def get_global_leaderboard(
    platform_id: Optional[int] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get global leaderboard"""
    
    query = select(PlatformProfile).where(
        PlatformProfile.global_rank.isnot(None)
    )
    
    if platform_id:
        query = query.where(PlatformProfile.platform_id == platform_id)
    
    query = query.order_by(PlatformProfile.global_rank).limit(limit)
    
    result = await db.execute(query)
    profiles = result.scalars().all()
    
    return profiles

