import json
import azure.functions as func
import requests
import json
from requests.api import request

# Create Order Function
    #
    # CALLED FROM:  Trading view
    #
    # FUNCTION:     This function goes to the database and grabs the refresh token and account id from the database then
    #               uses the refresh token to call the GET ACCESS TOKEN function for a fresh token
    #               Gets the data from the tradingview payload and formats a 
    #
    # PARAMS:       Refresh token, account id, ticker symbol, stock price, user id
    #
    #FUNCTION FLOW: 1. Get the auth token from `PythonAuth` azure function for each user
    #               3. Get the user account information to use for deciding how much to buy for the user
    #               4. Buy for each user based on their information in the database
    #               5. Send them a notification

def main(req: func.HttpRequest) -> func.HttpResponse:
    refresh_token = req.headers.get('refresh_token')
    account_id = str(req.headers.get('account_id'))
    ticker_symbol = req.headers.get('ticker_symbol')
    stock_price = int(req.headers.get('stock_price'))
    user_id = req.headers.get("user_id")

    access_token = get_access_token(refresh_token)
    shares_to_buy = calculateShares(access_token, account_id, stock_price)
    buy_response = buyOrder(access_token, str(account_id), ticker_symbol, shares_to_buy)

    if buy_response.status_code is 200 :
        requests.post("https://notifcationsfunctionapplication.azurewebsites.net/api/SendNotification?code=ffzsBnyso3Zfi7k7comwPWW5zwIRtJXruWpsAOxCXPFF1Ldp9rOPbQ==",
            headers = {
                "user_id" : user_id,
                "ticker_symbol" : ticker_symbol,
                "stock_price" : stock_price,
                "amount_bought" : shares_to_buy,
                "instruction" : "buy"
        })
        return func.HttpResponse("Successful buy")
    else :
        return func.HttpResponse(buy_response.text)

def get_access_token(refresh_token):
    headers = {
            'refresh_token': str(refresh_token)
        }
    account_reply = requests.get(r'https://tdameritradeauthentication.azurewebsites.net/api/PythonAuth?code=0cOSkySOqqJTP6usrrjaKlvWLdeGeBFFjS9sEO12b2ZBaHrzJh7OIA==', headers = headers)
    account_reply = account_reply.headers.get('access_token')
    return account_reply

def calculateShares(access_token,account_id,stock_price):
    # Get account data
    headers = { "Content-Type":"application/x-www-form-urlencoded" }
    payload = {
            'authorization':'Bearer ' + str(access_token)
        }
    
    account_reply = requests.get('https://api.tdameritrade.com/v1/accounts/'+account_id, headers = payload)

    response_json = account_reply.text
    
    # First Testing if an error is recieved.  If it is unable to be parsed to a json array an error was passed back
    try:
        response_json = json.loads(account_reply.text)
    except:
        return func.HttpResponse(body = "Incorrect code sent in through headers", status_code = 404)

    # Get the Securities Account
    security_account = response_json['securitiesAccount']

    #Get Buying Power
    buying_power = security_account['projectedBalances']['buyingPower']

    percentage_of_account = .15
    
    cash_for_trade = buying_power * percentage_of_account

    number_of_stock =  int(cash_for_trade / stock_price)

    return number_of_stock

def buyOrder(access_token, account_number, stock, shares_to_buy):

    headers = {
        'Content-Type':'application/json',
        'Authorization':'Bearer ' + str(access_token)
    }

    payload = {
            "orderType": "MARKET",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                "instruction": "Buy",
                "quantity": shares_to_buy,
                "instrument": {
                    "symbol": str(stock),
                    "assetType": "EQUITY"
                }
                }
            ]
    }
    url = 'https://api.tdameritrade.com/v1/accounts/%s/orders' % account_number
    response = requests.post(url, headers = headers, json=payload)
    
    return response