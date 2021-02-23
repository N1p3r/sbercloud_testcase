from contextlib import contextmanager
from typing import List
from pydantic import parse_obj_as
import uvicorn

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.validators import Invoice, IdRequestModel, DbInvoiceModel, Payment, \
    DbPaymentModel
from models.db import InvoiceORMModel, PaymentORMModel

app = FastAPI()

engine = create_engine("postgresql://postgres:12345@localhost:5432/app", echo=False)
session_factory = sessionmaker(bind=engine)


@contextmanager
def get_session_managed():
    session = session_factory()
    try:
        yield session
    except Exception:
        raise
    finally:
        session.close()


@app.post("/invoice/create", status_code=201, response_model=IdRequestModel)
async def create_invoice(invoice: Invoice):
    model = InvoiceORMModel(**invoice.dict())
    with get_session_managed() as sess:
        invoice_id = model.save(sess)
    return IdRequestModel(id=invoice_id)


@app.delete("/invoice/delete/{id}")
async def delete_invoice(id: int):
    with get_session_managed() as sess:
        try:
            model: InvoiceORMModel = InvoiceORMModel.get_by_id(sess, id)
            model.delete(sess)
        except ValueError:
            raise HTTPException(400, "Wrong invoice id")


@app.put("/invoice/paid/{id}", status_code=200)
async def set_paid(id: int):
    with get_session_managed() as sess:
        try:
            model: InvoiceORMModel = InvoiceORMModel.get_by_id(sess, id)
            model.set_paid(sess)
        except ValueError:
            raise HTTPException(400, "Wrong invoice id")


@app.get("/invoice/{id}")
async def get_invoice(id: int):
    with get_session_managed() as sess:
        try:
            model: InvoiceORMModel = InvoiceORMModel.get_by_id(sess, id)
        except ValueError:
            raise HTTPException(400, "Wrong invoice id")
        return DbInvoiceModel.from_orm(model)


@app.get("/invoice/users/{id}")
async def get_invoices(id: int):
    with get_session_managed() as sess:
        try:
            objs: InvoiceORMModel = InvoiceORMModel.get_by_user_id(sess, id)
            print(objs)
        except ValueError:
            raise HTTPException(400, "Wrong invoice id")
        response = parse_obj_as(List[DbInvoiceModel], [DbInvoiceModel.from_orm(i) for i in objs])
        return response


# payments

@app.post("/payment/create", status_code=201, response_model=IdRequestModel)
async def create_payment(payment: Payment):
    with get_session_managed() as sess:
        try:
            InvoiceORMModel.get_by_id(sess, payment.invoice_id)  # move to pydantic root_validator mb?
            model = PaymentORMModel(**payment.dict())
            payment_id = model.save(sess)
        except ValueError:
            raise HTTPException(400, "Wrong invoice id")
    return IdRequestModel(id=payment_id)


@app.delete("/payment/delete/{id}", status_code=200)
async def delete_payment(id: int):
    with get_session_managed() as sess:
        try:
            model: PaymentORMModel = PaymentORMModel.get_by_id(sess, id)
            model.delete(sess)
        except ValueError:
            raise HTTPException(400, "Wrong payment id")


@app.get("/payment/users/{id}")
async def get_payments(id: int):
    with get_session_managed() as sess:
        objs: List[PaymentORMModel] = PaymentORMModel.get_by_user_id(sess, id)
        response = parse_obj_as(List[DbPaymentModel], [DbPaymentModel.from_orm(i) for i in objs])
        return response


@app.get("/payment/{id}")
async def get_payment(id: int):
    with get_session_managed() as sess:
        try:
            model: DbPaymentModel = PaymentORMModel.get_by_id(sess, id)
        except ValueError:
            raise HTTPException(400, "Wrong payment id")
        return DbPaymentModel.from_orm(model)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
