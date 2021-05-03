import json
from requests import status_codes
from requests.adapters import HTTPResponse
from requests.sessions import HTTPAdapter
import azure.functions as func
import requests
import mysql.connector
import pathlib
import re

# GET USER DASHBOARD FUNCTION
#
# CALLED FROM:  On dashboard page initialization
#
# FUNCTION:     This Function is used to get the users access token from the database, use it to get user data from the TD API and return it to the website
#
# PARAMS:       header - <user_id> : Used to find the user in the database
#
# RESPONSE:     Returns the users TDA Account information in the body

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.headers.get('user_id')
    refresh_token = None
    access_token = None
    security_account = None

    regex = "([a-zA-Z0-9]){24}"

    not_valid_user_id = str(re.search(regex,user_id)) is None

    if not_valid_user_id:
        return func.HTTPResponse("No user id found", status_codes=404)

    cnx = mysql.connector.connect(
            user="AstraAlgo@astraalgoserv1", 
            password='Algoastra2020', 
            host="astraalgoserv1.mysql.database.azure.com", 
            port=3306,
            database = 'astraalgo',
            ssl_ca=get_ssl_cert()
        )

    cursor = cnx.cursor()
    query = '''select refresh_token
                from authentication
                where user_id = '%s' ''' % user_id
    cursor.execute(query)

    results = cursor.fetchall()
    refresh_token = results[0][0]

    headers = { 'refresh_token' : str(refresh_token) }
    url = "https://tdameritradeauthentication.azurewebsites.net/api/PythonAuth?code=0cOSkySOqqJTP6usrrjaKlvWLdeGeBFFjS9sEO12b2ZBaHrzJh7OIA=="

    response = requests.get(url, headers=headers)

    if(response.headers.get('status_code') is 500):
        return func.HttpResponse(str(response.get('error')))
    
    elif (response.headers.get('access_token') is not None) :
        access_token = response.headers.get('access_token')
    
        headers = {
            'Authorization':'Bearer ' + str(access_token)
        }
        params = {
            "fields" : "positions,orders" 
        }
        account_reply = requests.get(r'https://api.tdameritrade.com/v1/accounts', headers = headers, params = params)
        account_json = account_reply.text
    
        try:
            account_json = json.loads(account_reply.text)
            security_account = account_json[0]['securitiesAccount']
        except:
            return func.HttpResponse(body = "Incorrect code sent in through headers", status_code = 404)
    
        cursor.close()
        cnx.close()
        return func.HttpResponse(json.dumps(security_account))

def get_ssl_cert():
    current_path = pathlib.Path(__file__).parent.parent
    return str(current_path / 'BaltimoreCyberTrustRoot.crt.pem')