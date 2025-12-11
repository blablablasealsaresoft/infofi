"""Twitter-related models"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class TwitterProfile(Base):
    """Twitter profile model"""
    __tablename__ = "twitter_profiles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    twitter_handle = Column(String(100), unique=True, nullable=False)
    twitter_id = Column(String(50), unique=True, nullable=True)
    display_name = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    tweets_count = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    profile_image_url = Column(String(500), nullable=True)
    last_synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    engagements = relationship("TwitterEngagement", back_populates="profile", cascade="all, delete-orphan")
    shill_scores = relationship("ShillScore", back_populates="twitter_profile")


class TwitterEngagement(Base):
    """Twitter engagement model"""
    __tablename__ = "twitter_engagement"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    twitter_profile_id = Column(Integer, ForeignKey('twitter_profiles.id', ondelete='CASCADE'), nullable=False)
    tweet_id = Column(String(50), unique=True, nullable=False)
    tweet_text = Column(Text, nullable=True)
    posted_at = Column(DateTime, nullable=True)
    likes_count = Column(Integer, default=0)
    retweets_count = Column(Integer, default=0)
    replies_count = Column(Integer, default=0)
    quotes_count = Column(Integer, default=0)
    is_platform_related = Column(Boolean, default=False)
    related_platforms = Column(ARRAY(String(100)), nullable=True)
    sentiment = Column(String(20), nullable=True)  # positive, neutral, negative
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    profile = relationship("TwitterProfile", back_populates="engagements")

