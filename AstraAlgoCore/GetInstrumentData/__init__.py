from requests.adapters import HTTPResponse
from requests.models import HTTPError
import azure.functions as func
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    symbols = req.headers.get('symbols')
    params = {
        "apikey" : "NYDHGTAWWLQ47ZOO9OTDLVSTOGUVPYQX@AMER.OAUTHAP",
        "symbol" : symbols
    }
    account_reply = requests.get(r'https://api.tdameritrade.com/v1/marketdata/quotes', params = params)
    return func.HttpResponse(account_reply.text)