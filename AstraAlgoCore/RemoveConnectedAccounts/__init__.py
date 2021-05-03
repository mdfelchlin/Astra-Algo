import json
import azure.functions as func
import mysql.connector
import pathlib
import re

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.headers.get('user_id')
    account_to_remove = req.headers.get('account')

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
        if account_to_remove == 'TDA':
            query = ''' DELETE FROM authentication
                        WHERE user_id = '%s'; ''' % user_id
            cursor.execute(query)

            query = ''' UPDATE users
                        SET td_ameritrade_username = '' 
                        WHERE user_id = '%s'; ''' % user_id
            cursor.execute(query)

        elif account_to_remove == 'Discord':
            query = ''' UPDATE users
                        SET discord_user_id = '', discord_username = ''
                        WHERE user_id = '%s'; '''  % user_id
            cursor.execute(query)

            query = ''' UPDATE notification_pref
                        SET buy_discord = 0, sell_discord = 0
                        WHERE user_id = '%s'; ''' % user_id
            cursor.execute(query)

    except mysql.connector.Error as error :
        return func.HttpResponse(body=str(error), status_code=500)

    except :
        return func.HTTPResponse("Some other error")
    
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
    cnx.commit()
    cursor.close()
    cnx.close()

    return func.HttpResponse(json.dumps(user_data))
    
def get_ssl_cert():
    current_path = pathlib.Path(__file__).parent.parent
    return str(current_path / 'BaltimoreCyberTrustRoot.crt.pem')