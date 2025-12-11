"""Analytics models"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class ShillScore(Base):
    """Shill score model"""
    __tablename__ = "shill_scores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform_profile_id = Column(UUID(as_uuid=True), ForeignKey('platform_profiles.id', ondelete='CASCADE'), nullable=False)
    twitter_profile_id = Column(Integer, ForeignKey('twitter_profiles.id', ondelete='CASCADE'), nullable=False)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=True)
    score = Column(Numeric(5, 2), nullable=False)  # 0.00 to 100.00
    tweets_analyzed = Column(Integer, default=0)
    avg_engagement = Column(Integer, default=0)
    platform_correlation = Column(Numeric(3, 2), nullable=True)  # -1.00 to 1.00
    effectiveness_rating = Column(String(20), nullable=True)  # low, medium, high, elite
    calculated_at = Column(DateTime, default=func.now())
    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)
    
    # Relationships
    profile = relationship("PlatformProfile", back_populates="shill_scores")
    twitter_profile = relationship("TwitterProfile", back_populates="shill_scores")


class ROIPrediction(Base):
    """ROI prediction model"""
    __tablename__ = "roi_predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey('campaigns.id', ondelete='CASCADE'), nullable=False)
    model_version = Column(String(20), nullable=True)
    predicted_airdrop_value_usd = Column(Numeric(15, 2), nullable=True)
    predicted_time_investment_hours = Column(Numeric(10, 2), nullable=True)
    roi_per_hour = Column(Numeric(10, 2), nullable=True)
    confidence_score = Column(Numeric(3, 2), nullable=True)  # 0.00 to 1.00
    whale_concentration = Column(Numeric(3, 2), nullable=True)  # 0.00 to 1.00
    recommendation = Column(String(20), nullable=True)  # strong_buy, buy, hold, skip
    factors = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    campaign = relationship("Campaign", back_populates="roi_predictions")

