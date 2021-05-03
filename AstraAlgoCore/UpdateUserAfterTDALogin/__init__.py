import logging
import json
import time
import os
from os import access
from requests.adapters import HTTPResponse
from requests.models import HTTPError
import azure.functions as func
import requests
import urllib
import mysql.connector
import pathlib
from urllib.parse import unquote
import re


# UPDATE USER AFTER TD LOGIN FUNCTION 
#
# CALLED FROM:  When the user selects the login from the Account page
#
# FUNCTION:     This Function is used to get the users authentication credintials from TD Ameritrade
#               and then save them into the database
#
# PARAMS:       header - <code> : Used to be decoded and comes from TD Ameritrade after login
#               header - <user_id> : Used to find the user in the database
#
# RESPONSE:     Sends a 200 OK back if the user was successfully logged in

def main(req: func.HttpRequest) -> func.HttpResponse:
    code = None
    code_to_decode = None
    headers = None
    user_id = None
    td_account_id = 0

    code_to_decode = req.headers.get('code')
    user_id = req.headers.get('user_id')

    headers = {"Content-Type":"application/x-www-form-urlencoded"}

    regex = "([a-zA-Z0-9]){24}"
    not_valid_user_id = str(re.search(regex,user_id)) is None

    if (not_valid_user_id):
        return func.HTTPResponse("No user id found", status_codes=404)

    if (code_to_decode is not None):
        code = unquote(code_to_decode)
        payload = { 
            'grant_type': 'authorization_code', 
            'access_type': 'offline',
            'code': code, 
            'client_id': 'NYDHGTAWWLQ47ZOO9OTDLVSTOGUVPYQX@AMER.OAUTHAP',
            'redirect_uri': "https://localhost:44352/account/td"
            }
    else:
        return func.HttpResponse("No code was sent")
            
    auth_reply = requests.post(r'https://api.tdameritrade.com/v1/oauth2/token', headers = headers, data=payload)

    decoded_content = auth_reply.json()

    if(decoded_content.get('error') is not None):
        return func.HttpResponse(str(decoded_content.get('error')))
    else:
        refresh_token = str(decoded_content['refresh_token'])
        refresh_token_expiration = time.time() + 2629743
        access_token = str(decoded_content['access_token'])
        access_token_expiration = decoded_content['expires_in']

        headers = {
            'Authorization':'Bearer ' + str(access_token)
        }
        account_reply = (requests.get(r'https://api.tdameritrade.com/v1/accounts', headers = headers))
        response_json = account_reply.text

        try:
            response_json = json.loads(account_reply.text)
        except:
            return func.HttpResponse(body = "Incorrect code sent in through headers", status_code = 404)

        security_account = response_json[0]['securitiesAccount']
        td_account_id = int(security_account['accountId'])

        cnx = mysql.connector.connect(
            user="AstraAlgo@astraalgoserv1", 
            password='Algoastra2020', 
            host="astraalgoserv1.mysql.database.azure.com", 
            port=3306,
            database = 'astraalgo',
            ssl_ca=get_ssl_cert()
        )
        cursor = cnx.cursor()

        try:
            query = ''' REPLACE INTO authentication 
                                 (user_id, account_number, access_token, refresh_token, access_token_expiration, refresh_token_expiration) 
                                  VALUES(%s,%s,%s,%s,%s,%s); '''
            cursor.execute(query, (user_id, td_account_id, access_token, refresh_token, access_token_expiration, refresh_token_expiration))
            
            query = ''' UPDATE users
                        SET td_ameritrade_username = 't'
                        WHERE user_id = '%s'; '''  % user_id
            cursor.execute(query)

            cnx.commit()
        except mysql.connector.Error as error :
            return func.HttpResponse(str(error))

        try :
            query = ''' SELECT u.last_name, u.first_name, u.email, u.phone_number, u.discord_username, u.td_ameritrade_username, 
                            n.buy_text_message, n.buy_email, n.buy_discord, n.sell_text_message, n.sell_email, n.sell_discord 
                        FROM users AS u
                        LEFT JOIN notification_pref AS n ON u.user_id = n.user_id
                        WHERE u.user_id = '%s' ''' % user_id
            cursor.execute(query)
            data = cursor.fetchone()
        except mysql.connector.Error as error :
            return func.HttpResponse(body = str(error), status_code = 404)
        
        if (data is None) :
            return func.HttpResponse("User Account information does not exist")

        user_data = {
            "lastname" : data[0],
            "firstname" : data[1],
            "email" : data[2],
            "phoneNumber" : data[3],
            "discordUsername" : data[4],
            "tdAmeritradeUsername" : data[5],
            "buyTextMessage" : data[6],
            "buyEmail" : data[7],
            "buyDiscord" : data[8],
            "sellTextMessage" : data[9],
            "sellEmail" : data[10],
            "sellDiscord" : data[11]
        }
        cursor.close()
        cnx.close()

        return func.HttpResponse(json.dumps(user_data))

def get_ssl_cert():
    current_path = pathlib.Path(__file__).parent.parent
    return str(current_path / 'BaltimoreCyberTrustRoot.crt.pem')