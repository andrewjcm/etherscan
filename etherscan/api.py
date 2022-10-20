import requests
from etherscan.exceptions import check_for_error_status


class EtherscanApi:
    def __init__(self, api_key, uri="https://api.etherscan.io/api"):
        self.URI = uri
        self.API_KEY = api_key

    def get_ether_price(self):
        payload = {
            "module": "stats",
            "action": "ethprice",
            "apikey": self.API_KEY
        }
        r = requests.get(self.URI, payload)

        check_for_error_status(r, payload)
        return float(r.json()["result"]["ethusd"])

    def get_transactions(self, address):
        payload = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "apikey": self.API_KEY
        }
        r = requests.get(self.URI, params=payload)
        check_for_error_status(r, payload)
        return r.json()["result"]

    def get_erc20_transactions(self, address):
        payload = {
            "module": "account",
            "action": "tokentx",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "apikey": self.API_KEY
        }
        r = requests.get(self.URI, params=payload)
        check_for_error_status(r, payload)
        return r.json()["result"]

    def get_balance(self, address):
        payload = {
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest",
            "apikey": self.API_KEY
        }
        r = requests.get(self.URI, params=payload)
        check_for_error_status(r, payload)
        return int(r.json()["result"])

    def get_multiple_balances(self, addresses):
        payload = {
            "module": "account",
            "action": "balancemulti",
            "address": ",".join(addresses),
            "tag": "latest",
            "apikey": self.API_KEY
        }
        r = requests.get(self.URI, params=payload)
        check_for_error_status(r, payload)
        return r.json()["result"]
