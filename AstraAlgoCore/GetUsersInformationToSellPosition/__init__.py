import azure.functions as func
import requests
import mysql.connector
import pathlib

def main(req: func.HttpRequest) -> func.HttpResponse:
    ticker_symbol = req.headers.get('ticker_symbol')
    stock_price = req.headers.get('stock_price')

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
        "account_id" : account_id,
        "ticker_symbol" : ticker_symbol,
        "stock_price" : stock_price
        }
        response = requests.post(
            r'https://tdameritradeauthentication.azurewebsites.net/api/SellPosition?code=EX02guHYs5/mZ9GDT35PtKQBAhv0yfl34VJAIpoRgTJ2R5SjBFkR8A==', 
            headers = headers)

    cursor.close()
    cnx.close()

    return func.HttpRequest("200 OK")

def get_ssl_cert():
    current_path = pathlib.Path(__file__).parent.parent
    return str(current_path / 'BaltimoreCyberTrustRoot.crt.pem')