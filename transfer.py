from config import *
import requests
import random

headers = {
    "Rocket-Pay-Key": api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def generate_transfer(tg_id, amount_t):
    data_t = {
        "tgUserId": tg_id,
        "currency": "TON",
        "amount": amount_t,
        "transferId": str(random.randint(1, 100000000000000000)),
        "description": "KUBIKI by Rav"
    }
    return data_t


requests.post(f"{endpoint}app/transfer", headers=headers, json=generate_transfer(419471819, 100))
# print(requests.get(f"{endpoint}app/info", headers=headers).json()["data"]["balances"])
