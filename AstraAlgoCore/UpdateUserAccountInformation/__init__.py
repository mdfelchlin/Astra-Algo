import json
from requests import status_codes
from requests.adapters import HTTPResponse
from requests.sessions import HTTPAdapter
import azure.functions as func
import mysql.connector
import pathlib
import re

# UPDATE OR CREATE USER ACCOUNT INFORMATION
#
# CALLED FROM:  On account creation or when the user selects save
#
# FUNCTION:     This Function is used to save the users account information in the database and then if they do not exist then we create a record
#
# PARAMS:       header - <user_id> : Used to find the user in the database
#               lastName - Pased in value to be updated in the database
#               firstName - Pased in value to be updated in the database
#               email - Pased in value to be updated in the database
#               phoneNumber - Pased in value to be updated in the database
#               buyTextMessage - Pased in value to be updated in the database
#               buyEmail - Pased in value to be updated in the database
#               buyDiscord - Pased in value to be updated in the database
#               sellTextMessage - Pased in value to be updated in the database
#               sellEmail - Pased in value to be updated in the database
#               sellDiscord - Pased in value to be updated in the database
#
# RESPONSE:     Sends a 200 OK back if the users account was successfully updated in the database

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.headers.get('user_id')
    user_json = req.get_json()
    lastName = user_json['lastname']
    firstName = user_json['firstname']
    email = user_json['email']
    phoneNumber = user_json['phoneNumber']
    buyTextMessage = user_json['buyTextMessage']
    buyEmail = user_json['buyEmail']
    buyDiscord = user_json['buyDiscord']
    sellTextMessage = user_json['sellTextMessage']
    sellEmail = user_json['sellEmail']
    sellDiscord = user_json['sellDiscord']

    regex = "([a-zA-Z0-9]){24}"
    not_valid_user_id = str(re.search(regex, user_id)) is None

    if (not_valid_user_id):
        return func.HTTPResponse("No user id found", status_codes = 404)

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
        query = ''' REPLACE INTO users
                                (user_id, last_name, first_name, email, phone_number)
                                VALUES(%s,%s,%s,%s,%s); '''
        cursor.execute(query,(user_id, lastName, firstName, email, phoneNumber))

        query = ''' REPLACE INTO notification_pref
                                (user_id, buy_text_message, buy_email, buy_discord, sell_text_Message, sell_email, sell_discord) 
                                VALUES(%s,%s,%s,%s,%s,%s,%s); '''
        cursor.execute(query, (user_id, buyTextMessage, buyEmail, buyDiscord, sellTextMessage, sellEmail, sellDiscord))

    except mysql.connector.Error as error :
        return func.HttpResponse(body=str(error), status_code=500)

    except :
        return func.HTTPResponse("Some other error")
    
    cnx.commit()
    cnx.close()
    cursor.close()
    return func.HttpResponse(body="Successfully updated user")
    
def get_ssl_cert():
    current_path = pathlib.Path(__file__).parent.parent
    return str(current_path / 'BaltimoreCyberTrustRoot.crt.pem')