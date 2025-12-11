"""Database base configuration"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for Alembic
from app.models.user import User, UserWallet, UserSession  # noqa
from app.models.platform import Platform, Campaign, CampaignParticipation  # noqa
from app.models.profile import PlatformProfile  # noqa
from app.models.twitter import TwitterProfile, TwitterEngagement  # noqa
from app.models.analytics import ShillScore, ROIPrediction  # noqa
from app.models.alert import UserAlert, UserAlertPreferences  # noqa

