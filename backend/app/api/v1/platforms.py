"""Platform endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.platform import Platform
from app.schemas.platform import PlatformResponse

router = APIRouter()


@router.get("/", response_model=list[PlatformResponse])
async def list_platforms(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all platforms"""
    result = await db.execute(
        select(Platform).where(Platform.is_active == True).offset(skip).limit(limit)
    )
    platforms = result.scalars().all()
    return platforms

