import azure.functions as func
import requests
import mysql.connector
import pathlib
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    ticker_symbol = req.headers.get('symbol')
    stock_price = req.headers.get('price')

    cnx = mysql.connector.connect(
        user="AstraAlgo@astraalgoserv1", 
        password='Algoastra2020', 
        host="astraalgoserv1.mysql.database.azure.com", 
        port=3306,
        database = 'astraalgo',
        ssl_ca=get_ssl_cert()
    )
    
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM astraalgo.authentication;')
    result_list = cursor.fetchall()

    for row in result_list:
        user_id = row[0]
        account_id = row[1]
        refresh_token = row[3]
        headers = {
        "user_id" : user_id,
        "refresh_token" : refresh_token,
        "account_id" : (account_id),
        "ticker_symbol" : ticker_symbol,
        "stock_price" : stock_price
        }
        response = requests.post(
            r'https://tdameritradeauthentication.azurewebsites.net/api/BuyPosition?code=p7BBbHQE6Nz6t5QdYsVa3QnqGw2PoALadw6JMFU9YqxC0ZkCAUNcfQ==', 
            headers = headers)

        if response.status_code !=200:
            
            return func.HttpResponse(response.reason)

    cursor.close()
    cnx.close()


    return func.HttpResponse("200 OK")

def get_ssl_cert():
    current_path = pathlib.Path(__file__).parent.parent
    return str(current_path / 'BaltimoreCyberTrustRoot.crt.pem')