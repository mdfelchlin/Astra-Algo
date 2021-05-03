import json
from requests import status_codes
from requests.adapters import HTTPResponse
from requests.sessions import HTTPAdapter
import azure.functions as func
import requests
import mysql.connector
import pathlib
import re

# GET USER ACCOUNT INFORMATION
#
# CALLED FROM:  On account page initialization
#
# FUNCTION:     This Function is used to get the users account information to be displayed on the website
#
# PARAMS:       header - <user_id> : Used to find the user in the database
#
# RESPONSE:      Returns the users account information in the body

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.headers.get('user_id')
    data = None

    regex = "([a-zA-Z0-9]){24}"
    not_valid_user_id = str(re.search(regex,user_id)) is None

    if (not_valid_user_id):
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
    query = '''SELECT u.last_name, u.first_name, u.email, u.phone_number, u.discord_username, u.td_ameritrade_username, u.subscription_active,
                      n.buy_text_message, n.buy_email, n.buy_discord, n.sell_text_message, n.sell_email, n.sell_discord
               FROM users AS u
               LEFT JOIN notification_pref AS n ON u.user_id = n.user_id
               WHERE u.user_id = '%s' ''' % user_id
    
    try :
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
        "subscriptionActive" : data[6],
        "buyTextMessage" : data[7],
        "buyEmail" : data[8],
        "buyDiscord" : data[9],
        "sellTextMessage" : data[10],
        "sellEmail" : data[11],
        "sellDiscord" : data[12]
    }
    
    cursor.close()
    cnx.close()

    return func.HttpResponse(json.dumps(user_data))

def get_ssl_cert():
    current_path = pathlib.Path(__file__).parent.parent
    return str(current_path / 'BaltimoreCyberTrustRoot.crt.pem')