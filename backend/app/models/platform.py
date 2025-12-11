"""Platform and campaign models"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class Platform(Base):
    """Platform model"""
    __tablename__ = "platforms"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    domain = Column(String(255), nullable=False)
    icon_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    crawler_config = Column(JSONB, default={})
    last_crawled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="platform")
    profiles = relationship("PlatformProfile", back_populates="platform")


class Campaign(Base):
    """Campaign model"""
    __tablename__ = "campaigns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    external_id = Column(String(255), nullable=True)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(1000), nullable=True)
    campaign_type = Column(String(50), nullable=True)  # quest, tournament, airdrop
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    total_participants = Column(Integer, default=0)
    total_rewards_usd = Column(Numeric(15, 2), nullable=True)
    min_points_required = Column(Integer, nullable=True)
    status = Column(String(20), default='active')  # active, ended, upcoming
    discovered_at = Column(DateTime, default=func.now())
    metadata = Column(JSONB, default={})
    
    # Relationships
    platform = relationship("Platform", back_populates="campaigns")
    participations = relationship("CampaignParticipation", back_populates="campaign")
    roi_predictions = relationship("ROIPrediction", back_populates="campaign")


class CampaignParticipation(Base):
    """Campaign participation model"""
    __tablename__ = "campaign_participation"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey('campaigns.id', ondelete='CASCADE'), nullable=False)
    platform_profile_id = Column(UUID(as_uuid=True), ForeignKey('platform_profiles.id', ondelete='CASCADE'), nullable=False)
    points_earned = Column(Numeric(15, 2), default=0)
    rank = Column(Integer, nullable=True)
    completion_percentage = Column(Numeric(5, 2), nullable=True)
    quests_completed = Column(Integer, default=0)
    quests_total = Column(Integer, nullable=True)
    first_activity_at = Column(DateTime, nullable=True)
    last_activity_at = Column(DateTime, nullable=True)
    metadata = Column(JSONB, default={})
    
    # Relationships
    campaign = relationship("Campaign", back_populates="participations")
    profile = relationship("PlatformProfile", back_populates="participations")

