import aiohttp
from os import getenv

api_url = getenv("API_URL")
json_headers = {"content-type": "application/json"}


def get_invoice_id(invoice_id: int):
    async with aiohttp.ClientSession(timeout=10, raise_for_status=True, headers=json_headers) as sess:
        response = await sess.get(f"{api_url}/invoice/{invoice_id}")
        invoice = await response.json()
    return invoice


def get_invoices_by_user_id(user_id: int):
    async with aiohttp.ClientSession(timeout=10, raise_for_status=True, headers=json_headers) as sess:
        response = await sess.get(f"{api_url}/invoice/users/{user_id}")
        invoice_list = await response.json()
    return invoice_list


def get_payment_by_id(payment_id: int):
    async with aiohttp.ClientSession(timeout=10, raise_for_status=True, headers=json_headers) as sess:
        response = await sess.get(f"{api_url}/payment/{payment_id}")
        payment = await response.json()
    return payment


def get_payments_by_user_id(user_id: int):
    async with aiohttp.ClientSession(timeout=10, raise_for_status=True, headers=json_headers) as sess:
        response = await sess.get(f"{api_url}/payment/users/{user_id}")
        payments = await response.json()
    return payments
