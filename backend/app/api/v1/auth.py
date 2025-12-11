"""Authentication endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User, UserWallet, UserSession
from app.schemas.user import (
    UserCreate, UserLogin, UserResponse, 
    TokenResponse, WalletLogin, UserWalletCreate
)
from app.core.security import (
    get_password_hash, verify_password,
    create_access_token, create_refresh_token,
    verify_wallet_signature, get_current_user
)

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register new user with email/password"""
    
    # Check if email exists
    if user_data.email:
        result = await db.execute(select(User).where(User.email == user_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check if username exists
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=get_password_hash(user_data.password) if user_data.password else None
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login with email/password"""
    
    # Get user
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()
    
    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Save session
    session = UserSession(
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(session)
    await db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/wallet-login", response_model=TokenResponse)
async def wallet_login(wallet_data: WalletLogin, db: AsyncSession = Depends(get_db)):
    """Login with Web3 wallet signature"""
    
    # Verify signature
    if not verify_wallet_signature(
        wallet_data.wallet_address,
        wallet_data.message,
        wallet_data.signature
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature"
        )
    
    # Get or create wallet
    result = await db.execute(
        select(UserWallet).where(UserWallet.wallet_address == wallet_data.wallet_address)
    )
    wallet = result.scalar_one_or_none()
    
    if not wallet:
        # Create new user and wallet
        user = User(username=f"user_{wallet_data.wallet_address[:8]}")
        db.add(user)
        await db.flush()
        
        wallet = UserWallet(
            user_id=user.id,
            wallet_address=wallet_data.wallet_address,
            is_primary=True,
            verified_at=datetime.utcnow()
        )
        db.add(wallet)
        await db.commit()
        await db.refresh(wallet)
    
    user = await db.get(User, wallet.user_id)
    
    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Logout user"""
    # Delete user sessions
    await db.execute(delete(UserSession).where(UserSession.user_id == current_user.id))
    await db.commit()
    
    return {"message": "Logged out successfully"}


from datetime import datetime, timedelta
from sqlalchemy import delete

