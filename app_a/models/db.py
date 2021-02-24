from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

base = declarative_base()


class BaseOrmModel(base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False)

    @classmethod
    def get_by_id(cls, session: Session, id: int):
        obj = session.query(cls).get(id)
        if not obj:
            raise ValueError(f"Object with id {id} not found")
        return obj

    def save(self, session: Session):
        session.add(self)
        session.commit()
        return self.id

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

    @classmethod
    def get_by_user_id(cls, session: Session, user_id: int):
        models = session.query(cls).filter(cls.user_id == user_id).all()
        return models


class InvoiceORMModel(BaseOrmModel):
    __tablename__ = "invoice"
    """Исходим из того, что всеми рассчётами занимается
    внешний сервис, наша задача регистрация счетов и статуса их оплаты"""
    creation_date = Column(DateTime, nullable=False)
    cost = Column(Integer, nullable=False)
    currency = Column(String(20), nullable=False)

    @staticmethod
    def create_invoice(session: Session, cost: int,
                       currency: str,
                       creation_date: datetime = datetime.utcnow()):
        model = InvoiceORMModel(cost=cost, creation_date=creation_date, currency=currency)
        model.save(session)
        return True

    def set_paid(self, session: Session):
        payment = PaymentORMModel.create_payment(session=session,
                                                 user_id=self.user_id,
                                                 amount=self.cost,
                                                 timestamp=datetime.utcnow(),
                                                 invoice_id=self.id,
                                                 currency=self.currency)


class PaymentORMModel(BaseOrmModel):
    __tablename__ = "payment"
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    invoice_id = Column(ForeignKey(InvoiceORMModel.id), nullable=False)
    currency = Column(String(20), nullable=False)

    @classmethod
    def create_payment(cls, session: Session,
                       user_id: int,
                       amount: int,
                       currency: str,
                       invoice_id: int,
                       timestamp: datetime = datetime.utcnow()):
        payment = PaymentORMModel(user_id=user_id,
                                  invoice_id=invoice_id, amount=amount,
                                  timestamp=timestamp,
                                  currency=currency)
        payment.save(session)
