from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.db import LocalAsyncSession, get_session
from .utils import get_current_user_id
from app.models.user import (
    UserRead,
    UserCreate,
    UserUpdate,
)
from app.models.currency import CurrencyRead
from app.cruds.user import (
    get_user_by_id,
    get_users,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter()


@router.get("/users", tags=["users"], response_model=list[UserRead])
async def get_users_list(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not not found")
    return await get_users(db)


@router.get(
    "/users/me",
    tags=["users"],
    response_model=UserRead,
)
async def get_user(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    user = await get_user_by_id(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.post(
    "/users/me",
    tags=["users"],
    response_model=UserRead,
)
async def create_new_user(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user: UserCreate,
):  # Make only for admins
    return await create_user(db, user)


@router.put(
    "/users/me",
    tags=["users"],
    response_model=UserRead,
)
async def update_existing_user(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    user: UserUpdate,
):
    updated = await update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete(
    "/users/me",
    tags=["users"],
    response_model=UserRead,
)
async def delete_existing_user(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted
