from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from passlib.context import CryptContext
from decimal import Decimal

from app.models.currency import Currency, CurrencyRead


class UserBase(SQLModel):
    username: str
    email: str
    name: str
    surname: str
    fathers_name: Optional[str] = None
    deposit_quantity: int = Field(default=0)
    total_deposit: Decimal = Field(default=0, max_digits=5, decimal_places=3)
    total_withdrawal: Decimal = Field(default=0, max_digits=5, decimal_places=3)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: Optional[str] = Field(default=None, unique=True)
    currencies: list[Currency] = Relationship(back_populates="user")
    is_superuser: bool = False
    hashed_password: str = Field(nullable=False)

    @staticmethod
    def hash_password(password: str):
        """Encrypt password with bcrypt"""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    def validate_password(self, password: str):
        """Validate password with existing hash"""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.hashed_password)

    @property
    def full_name(self):
        return f"{self.surname} {self.name} {self.fathers_name}"


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    currencies: list[CurrencyRead] = []


class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    deposit_quantity: Optional[int] = None
    total_deposit: Optional[Decimal] = None
    total_withdrawal: Optional[Decimal] = None
