"""Alert models"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class UserAlert(Base):
    """User alert model"""
    __tablename__ = "user_alerts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    alert_type = Column(String(50), nullable=False)  # new_campaign, rank_change, whale_alert
    priority = Column(String(20), default='medium')  # low, medium, high, critical
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    related_entity_type = Column(String(50), nullable=True)  # campaign, profile, platform
    related_entity_id = Column(String(100), nullable=True)
    is_read = Column(Boolean, default=False)
    delivered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="alerts")


class UserAlertPreferences(Base):
    """User alert preferences model"""
    __tablename__ = "user_alert_preferences"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    email_enabled = Column(Boolean, default=True)
    telegram_enabled = Column(Boolean, default=False)
    telegram_chat_id = Column(String(50), nullable=True)
    push_enabled = Column(Boolean, default=False)
    alert_types = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

