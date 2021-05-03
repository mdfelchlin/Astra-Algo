import logging
import json
import azure.functions as func
import requests
import mysql.connector
import pathlib

# Create SellOrder Function
    #
    # CALLED FROM:  Trading view
    #
    # FUNCTION:     This function goes to the database and grabs the refresh token and account id from the database then
    #               uses the refresh token to call the GET ACCESS TOKEN function for a fresh token
    #               Gets the data from the tradingview payload and formats a 
    #
    # PARAMS:       Stock, price, 
    #
    #FUNCTION FLOW: 1. CALL TO DB TO GRAB ALL USER ID / ACCOUNT NUMBER / REFRESH TOKEN TUPLES
    #               2. Get the auth token from `PythonAuth` azure function for each user
    #               3. Get the user account information to use for deciding how much to sell for the user
    #               4. Sell for each user based on their information in their account
    #               5. Send them a notification

def main(req: func.HttpRequest) -> func.HttpResponse:
    refresh_token = req.headers.get('refresh_token')
    account_id = req.headers.get('account_id')
    stock = req.headers.get('stock')
    stock_price = req.headers.get('stock_price')
    user_id = req.headers.get("user_id")

    access_token = get_access_token(refresh_token)
    cancel_working_order(access_token,account_id,stock)
    shares_to_sell = calculateShares(access_token,account_id,stock)
    
    if(shares_to_sell != 0):
        sell_response = sellOrder(access_token,str(account_id),stock,shares_to_sell)

        if sell_response.status_code is 200:
            requests.post("https://notifcationsfunctionapplication.azurewebsites.net/api/SendNotification?code=ffzsBnyso3Zfi7k7comwPWW5zwIRtJXruWpsAOxCXPFF1Ldp9rOPbQ==",
            headers = {
                "user_id" : user_id,
                "ticker_symbol" : stock,
                "stock_price" : stock_price,
                "amount_bought" : shares_to_sell,
                "instruction" : "sell"
            })
            return func.HttpResponse("Successful Sell")
        else :
            return func.HttpResponse(sell_response.text)

    else:
        return func.HttpResponse("No shares to be Sold")
    
def get_access_token(refresh_token):
    headers = {
            'refresh_token': str(refresh_token)
        }
    account_reply = (requests.get(r'https://tdameritradeauthentication.azurewebsites.net/api/PythonAuth?code=0cOSkySOqqJTP6usrrjaKlvWLdeGeBFFjS9sEO12b2ZBaHrzJh7OIA==', headers = headers))
    account_reply = account_reply.headers.get('access_token')
    return account_reply

def cancel_working_order(access_token,account_id,stock):
    headers = {
            'Authorization':'Bearer ' + str(access_token),
            'fields': 'positions, orders'
        }
    payload = {
            'accountId': account_id, 
            'status' : 'WORKING'
        }

    account_reply = requests.get('https://api.tdameritrade.com/v1/orders', headers = headers, json= payload)
    response_json = account_reply.text
    
    try:
        response_json = json.loads(account_reply.text)
    except:
        return func.HttpResponse(body = "Incorrect code sent in through headers", status_code = 404)

    for order in response_json:
        if stock == order['orderLegCollection'][0]['instrument']['symbol']:
            try:

                working_order_id = order['orderId']

                headers = {
                'Authorization':'Bearer ' + str(access_token),
                }

                requests.delete('https://api.tdameritrade.com/v1/accounts/'+account_id+'/orders/'+str(working_order_id), headers = headers)

            except:
               return func.HttpResponse('ERROR CANCELING ORDER')

def calculateShares(access_token,account_id,stock):
    headers = {
            'Authorization':'Bearer ' + str(access_token),
        }
    payload = {
            'fields' : 'positions'
        }
    account_reply = requests.get('https://api.tdameritrade.com/v1/accounts', headers = headers, params= payload)

    try:
        response_json = json.loads(account_reply.text)
    except:
        return func.HttpResponse(body = "Incorrect code sent in through headers", status_code = 404)

    #TODO Check the response to see if we have shares in the stock we need to sell and how many of them we have
    for positions in response_json[0]['securitiesAccount']['positions']:
        
        if stock == positions['instrument']['symbol']:
            return str(positions['longQuantity'])
    
    return "0"

def sellOrder(access_token,account_number,stock,shares_to_sell):
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
                "instruction": "Sell",
                "quantity": str(shares_to_sell),
                "instrument": {
                    "symbol": str(stock),
                    "assetType": "EQUITY"
                }
                }
            ]
    }

    url = 'https://api.tdameritrade.com/v1/accounts/%s/orders' % account_number

    return requests.post(url, headers = headers, json=payload)