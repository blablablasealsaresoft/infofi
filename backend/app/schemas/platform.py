"""Platform schemas"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
from decimal import Decimal
from uuid import UUID


class PlatformBase(BaseModel):
    name: str
    domain: str
    icon_url: Optional[str] = None


class PlatformResponse(PlatformBase):
    id: int
    is_active: bool
    last_crawled_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    campaign_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    total_rewards_usd: Optional[Decimal] = None


class CampaignResponse(CampaignBase):
    id: UUID
    platform_id: int
    external_id: Optional[str]
    total_participants: int
    status: str
    discovered_at: datetime
    platform: Optional[PlatformResponse] = None
    
    class Config:
        from_attributes = True


class CampaignListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    campaigns: list[CampaignResponse]

