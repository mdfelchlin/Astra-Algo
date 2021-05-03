import azure.functions as func
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    chart = req.headers.get("chart")
    price = int(req.headers.get("price"))
    symbol = req.headers.get("symbol")
    instruction = req.headers.get("instruction")
    passphrase = req.headers.get("passphrase")

    if chart is None :
        return func.HttpResponse("No chart passed")
    if int(price) <= 0 :
        return func.HttpResponse("Invalid price")
    if symbol is None :
        return func.HttpResponse("No symbol passed for trading")
    if instruction is None :
        return func.HttpResponse("No instruction passed")
    if passphrase is None :
        return func.HttpResponse("No passphrase passed")

    if instruction == "Buy":
        buy_headers = {
            "Content-Type":"application/json",
            "stock" : str(symbol),
            "stock_price" : price,
            "chart" : chart
            }
        requests.post(
            r'https://tdameritradeauthentication.azurewebsites.net/api/GetUsersInformationToBuyPosition?code=Ihsw4zjbHLdaTmfwwjjKu0V0bBIrKT2EDQD96BZgJJVG1AOkBCLDpQ==', 
            headers = buy_headers)

    elif instruction == "Sell":
        sell_headers = {
            "Content-Type":"application/json",
            "stock" : str(symbol),
            "chart" : chart
            }
        requests.post(
            r'https://tdameritradeauthentication.azurewebsites.net/api/GetUsersInformationToSellPosition?code=MBE0BvdZopsUII9LvOPpfbi3OxuWmF4hle9UsctSdYOLHADirDqX3g==', 
            headers = sell_headers)

    return func.HttpResponse("200 OK")