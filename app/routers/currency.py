from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.db import LocalAsyncSession, get_session
from app.models.currency import(
    CurrencyRead,
    CurrencyCreate,
    CurrencyUpdate
)
from app.cruds.currency import (
    get_currencies,
    get_currency_by_id,
    get_currency_by_name,
    get_currency_by_code,
    create_currency,
    update_currency,
    delete_currency
)
from .utils import get_current_user_id


router = APIRouter()


@router.get(
    "/currencies/list",
    tags=["currencies"],
    reponse_model=list[CurrencyRead]
)
async def currencies_list(db: Annotated[LocalAsyncSession, Depends(get_session)]):
    return await get_currencies(db)


@router.get(
    "/currencies/{currency_id}",
    tags=["currencies"],
    reponse_model=CurrencyRead
)
async def currency_by_id(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    currency_id: int
):
    currency = await get_currency_by_id(db, currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return CurrencyRead.model_validate(currency)


@router.post(
    "/currencies",
    tags=["currencies"],
    response_model=CurrencyRead
)
async def create_currency_req(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    currency: CurrencyCreate
)
    db_currency = await create_currency(db, currency)
    return CurrencyRead.model_validate(db_currency)


@router.put(
    "/currencies",
    tags=["currencies"],
    response_model=CurrencyRead
)
async def create_currency_req(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    currency: CurrencyUpdate
)
    db_currency = await update_currency(db, currency)
    return CurrencyRead.model_validate(db_currency)
