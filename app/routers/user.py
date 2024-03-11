from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.db import LocalAsyncSession, get_session
from .utils import get_current_user_id
from app.models.user import (
    User,
    UserRead,
    UserCreate,
    UserUpdate,
    UserSideBarRead,
    AvatarUpload,
    AvatarDownload,
)
from app.cruds.user import (
    get_user_by_id,
    get_user_by_email,
    get_users,
    get_or_create_user_by_email,
    create_user,
    update_user,
    delete_user,
    update_user_kwargs,
)
from .utils import (
    upload_avatar,
    get_avatar,
)

router = APIRouter()


@router.get(
    "/users/me/sidebar_user",
    tags=["users"],
    response_model=UserSideBarRead,
)
async def get_sidebar_user(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    usb = UserSideBarRead.model_validate(user)
    usb.avatar_b64 = await get_avatar(user.avatar_filename)
    return usb


@router.post(
    "/users/me/upload_avatar",
    tags=["users"],
    response_model=UserRead,
)
async def upload_avatar_api(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    avatar: AvatarUpload,
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    avatar_filename = await upload_avatar(user.id, avatar)
    updated = await update_user(
        db, user.id, UserUpdate(avatar_filename=avatar_filename)
    )
    return UserRead.model_validate(updated)


@router.get("/users/me/currencies", tags=["users"], response_model=UserRead)


@router.get("/users/me/download_avatar", tags=["users"], response_model=AvatarDownload)
async def download_avatar_api(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    avatar_b64 = await get_avatar(user.avatar_filename)
    return AvatarDownload(avatar_b64=avatar_b64)


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
