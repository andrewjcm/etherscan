import csv
import time
from dotenv import dotenv_values
from etherscan.api import EtherscanApi

env = dotenv_values(".env")
API_KEY = env["API_KEY"]
WEI_ETH = 0.000000000000000001


def get_transaction_trends(address):
    def update_dict(dict_to_mod, transactions_obj, to_from_key, usd_value):
        address_str = transactions_obj[to_from_key]
        if address_str not in dict_to_mod:
            dict_to_mod[address_str] = {
                "out_value": 0,
                "in_value": 0,
                "out_count": 0,
                "in_count": 0,
                "total_value": 0,
                "total_count": 0
            }
        if to_from_key == "to":
            dict_to_mod[address_str]["out_value"] += usd_value
            dict_to_mod[address_str]["out_count"] += 1
        elif to_from_key == "from":
            dict_to_mod[address_str]["in_value"] += usd_value
            dict_to_mod[address_str]["in_count"] += 1
        dict_to_mod[address_str]["total_value"] += usd_value
        dict_to_mod[address_str]["total_count"] += 1

    def process_transactions(transactions, address, eth_usd):
        def calc_usd_from_wei(wei):
            return float(wei) * WEI_ETH * eth_usd

        trans = {}
        for t in transactions:
            usd_val = calc_usd_from_wei(t["value"])
            to_from_value = "to" if t["from"] == address.lower() else "from"
            update_dict(trans, t, to_from_value, usd_val)

        headers = [
            "address",
            "in_value",
            "in_count",
            "out_value",
            "out_count",
            "total_value",
            "total_count"
        ]
        with open(f"output/transaction_trends_{address}.csv", "w", newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(headers)
            for add in trans:
                row = [add]
                for header in headers[1:]:
                    row.append(trans[add][header])
                w.writerow(row)

    api = EtherscanApi(api_key=API_KEY)
    transactions = api.get_transactions(address)
    ETH_USD = api.get_ether_price()

    if type(transactions) == list:
        process_transactions(transactions, address, ETH_USD)
    elif type(transactions) == str:
        raise TypeError("Sorry buddy, there was an error with the api: " + transactions)
    else:
        raise TypeError("Who the fuck knows what happened? Maybe this is a clue: " + transactions)


def main():
    addresses = []
    with open("wallets.txt", "r") as f:
        wallet = f.readlines()
        for address in wallet:
            addresses.append(address.strip())

    for address in addresses:
        time.sleep(0.5)
        try:
            get_transaction_trends(address)
        except TypeError as e:
            print(e)


if __name__ == "__main__":
    main()
