class EtherscanApiError(Exception):
    pass


def check_for_error_status(response, payload):
    json_response = response.json()
    if int(json_response["status"]) == 0 and json_response["message"] != "No transactions found":
        raise EtherscanApiError(
            f"{json_response['message']}\nResult: {json_response['result']}\nPayload: {payload}"
        )


