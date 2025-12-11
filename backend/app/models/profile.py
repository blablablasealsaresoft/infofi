"""Platform profile models"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class PlatformProfile(Base):
    """Platform profile model"""
    __tablename__ = "platform_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_wallet_id = Column(Integer, ForeignKey('user_wallets.id', ondelete='CASCADE'), nullable=True)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    external_user_id = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True)
    display_name = Column(String(255), nullable=True)
    profile_url = Column(String(1000), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    total_points = Column(Numeric(15, 2), default=0)
    global_rank = Column(Integer, nullable=True)
    level = Column(Integer, nullable=True)
    twitter_handle = Column(String(100), nullable=True)
    discord_handle = Column(String(100), nullable=True)
    last_synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    metadata = Column(JSONB, default={})
    
    # Relationships
    wallet = relationship("UserWallet", back_populates="platform_profiles")
    platform = relationship("Platform", back_populates="profiles")
    participations = relationship("CampaignParticipation", back_populates="profile")
    shill_scores = relationship("ShillScore", back_populates="profile")

