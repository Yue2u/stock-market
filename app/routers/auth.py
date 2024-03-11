from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.models.user import (
    UserCreate,
)
from app.models.auth import Token
from app.cruds.user import get_user_by_email, create_user
from app.db import LocalAsyncSession, get_session
from .utils import create_token

router = APIRouter()


@router.post(
    "/users/login",
    tags=["users", "auth"],
    response_model=Token,
)
async def login_for_token(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    http_exception = HTTPException(
        status_code=400,
        detail="Incorrect email or password",
        headers={"Authorization": "Bearer"},
    )
    user = await get_user_by_email(db, form_data.username)
    if not user:
        raise http_exception
    if not user.validate_password(form_data.password):
        raise http_exception
    token = create_token(data={"sub": user.email})
    return Token(access_token=token)


@router.post(
    "/users/register",
    tags=["users", "auth"],
    response_model=Token,
)
async def register_user(
    db: Annotated[LocalAsyncSession, Depends(get_session)], user: UserCreate
):
    old_user = await get_user_by_email(db, user.email)
    if old_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(db, user)
    token = create_token(data={"sub": new_user.id})
    return Token(access_token=token)
