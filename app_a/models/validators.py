from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class IdRequestModel(BaseModel):
    id: int


class Invoice(BaseModel):
    user_id: int
    cost: int
    creation_date: Optional[datetime] = datetime.utcnow()
    currency: Optional[str] = "RUB"


class Payment(BaseModel):
    invoice_id: int
    user_id: int
    amount: int
    currency: Optional[str] = "RUB"
    timestamp: Optional[datetime]


class DbRecordModel(BaseModel):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class DbInvoiceModel(DbRecordModel):
    creation_date: datetime
    cost: int
    currency: str


class DbPaymentModel(DbRecordModel):
    amount: int
    user_id: int
    timestamp: datetime
    invoice_id: int
    currency: str
