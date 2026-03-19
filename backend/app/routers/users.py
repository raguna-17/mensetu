from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from argon2 import PasswordHasher
from jose import jwt
from argon2.exceptions import VerifyMismatchError

from app.db import get_db
from app.models import User
from app.schemas import UserCreate, UserRead, UserLogin
from app.auth import create_access_token, get_current_user, ph, JWT_ALGORITHM, JWT_SECRET_KEY

router = APIRouter(prefix="/api/v1/users", tags=["users"])

# ユーザー登録
@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = ph.hash(user_in.password)
    new_user = User(email=user_in.email, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# ログイン
@router.post("/login")
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
        ph.verify(user.hashed_password, user_in.password)
    except VerifyMismatchError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# 現在のユーザー取征E
@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

