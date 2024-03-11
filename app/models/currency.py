from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal


class CurrencyBase(SQLModel):
    name: str
    code: str
    symbol: str
    price: Decimal = Field(default=0, max_digits=5, decimal_places=3)  # in dollars
    price_date: str
    price_time: str

    user_id: int = Field(foreign_key="user.id")


class Currency(CurrencyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: "User" = Relationship(back_populates="currencies")


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyRead(SQLModel):
    id: int
    name: str
    code: str
    symbol: str
    price: Decimal
    price_date: str
    price_time: str


class CurrencyUpdate(SQLModel):
    name: Optional[str] = None
    code: Optional[str] = None
    symbol: Optional[str] = None
    price: Optional[Decimal] = None
    price_date: Optional[str] = None
    price_time: Optional[str] = None
