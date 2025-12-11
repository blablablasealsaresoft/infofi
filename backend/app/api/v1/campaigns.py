"""Campaign endpoints"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import UUID

from app.db.session import get_db
from app.models.platform import Campaign
from app.schemas.platform import CampaignResponse, CampaignListResponse

router = APIRouter()


@router.get("/", response_model=CampaignListResponse)
async def list_campaigns(
    platform_id: Optional[int] = None,
    status: Optional[str] = Query("active", regex="^(active|ended|upcoming)$"),
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """List campaigns with filters"""
    
    # Build query
    query = select(Campaign)
    
    if platform_id:
        query = query.where(Campaign.platform_id == platform_id)
    if status:
        query = query.where(Campaign.status == status)
    
    # Get total count
    count_query = select(func.count()).select_from(Campaign)
    if platform_id:
        count_query = count_query.where(Campaign.platform_id == platform_id)
    if status:
        count_query = count_query.where(Campaign.status == status)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get campaigns
    query = query.offset(skip).limit(limit).order_by(Campaign.discovered_at.desc())
    result = await db.execute(query)
    campaigns = result.scalars().all()
    
    return {
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "campaigns": campaigns
    }


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get campaign by ID"""
    campaign = await db.get(Campaign, campaign_id)
    return campaign

