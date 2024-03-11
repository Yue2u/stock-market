from app.db import LocalAsyncSession, get_session
from sqlmodel import select
from app.models.currency import (
    Currency,
    CurrencyCreate,
    CurrencyRead,
    CurrencyUpdate
)


async def get_currencies(db: LocalAsyncSession):
    currencies = await db.execute(select(Currency))
    return currencies.scalars().all()


async def get_currency_by_id(db: LocalAsyncSession, id: int):
    stmt = select(Currency).where(Currency.id == id)
    currencies = await db.execute(stmt)
    result = currencies.scalars().first()
    return result


async def get_currency_by_name(db: LocalAsyncSession, name: str):
    stmt = select(Currency).where(Currency.name == name)
    currencies = await db.execute(stmt)
    result = currencies.scalars().first()
    return result


async def get_currency_by_code(db: LocalAsyncSession, code: str):
    stmt = select(Currency).where(Currency.code == code)
    currencies = await db.execute(stmt)
    result = currencies.scalars().first()
    return result


async def create_currency(db: LocalAsyncSession, currency: CurrencyCreate):
    db_currency = Currency.model_validate(currency)
    db.add(db_currency)
    await db.commit()
    await db.refresh(db_currency)
    return db_currency


async def update_currency(db: LocalAsyncSession, id: int, currency: CurrencyUpdate):
    db_currency = await get_currency_by_id(db, id=id)
    if not db_currency:
        return None
    currency_data = currency.model_dump(exclude_unset=True)

    for key, value in currency_data.items():
        setattr(db_currency, key, value)

    db.add(db_currency)
    await db.commit()
    await db.refresh(db_currency)
    return db_currency


async def update_currency_kwargs(db: LocalAsyncSession, id: int, **kwargs):
    db_currency = await get_currency_by_id(db, id=id)
    if not db_currency:
        return None

    currency_data = kwargs
    for key, value in currency_data:
        setattr(db_currency, key, value)

    db.add(db_currency)
    await db.commit()
    await db.refresh(db_currency)
    return db_currency


async def delete_currency(db: LocalAsyncSession, id: int):
    db_currency = await get_currency_by_id(db, id=id)
    if not db_currency:
        return None
    await db.delete(db_currency)
    await db.commit()
    return db_currency