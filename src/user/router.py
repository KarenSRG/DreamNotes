from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.user import dao
from src.user.auth import create_access_token
from src.user.dao import get_user_by_username
from src.user.schema import UserCreate, UserResponse, Token
from src.utils.password_hashing import verify_password

router = APIRouter()


@router.post("/users/token", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
) -> Token:
    user = await get_user_by_username(db, form_data.username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=UserResponse)
async def create_user(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await dao.create_user(db, user)


@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user_by_id(
        user_id: int,
        db: AsyncSession = Depends(get_db)
) -> UserResponse:
    user = await dao.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
