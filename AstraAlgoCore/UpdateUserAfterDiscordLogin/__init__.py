import azure.functions as func
import requests
import mysql.connector
import pathlib
import json
import re

# UPDATE USER AFTER DISCORD LOGIN FUNCTION 
#
# CALLED FROM:  When the user selects the login from the Account page
#
# FUNCTION:     This Function is used to get the users id from discord to be able to send them messages
#
# PARAMS:       header - <code> : Used to be get the access token and then user information
#               header - <user_id> : Used to find the user in the database
#
# RESPONSE:     Sends a 200 OK back if the user was successfully logged in

API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_ID = '809190579610058823'
CLIENT_SECRET = 'ImzW_N06h0tIv_7w7DbRYyMShfT_MZOq'
REDIRECT_URI = 'https://localhost:44352/account/discord/'

def main(req: func.HttpRequest) -> func.HttpResponse:
    code = None
    headers = None
    user_id = None

    code = req.headers.get('code')
    user_id = str(req.headers.get('user_id'))

    if user_id == None :
        return func.HttpResponse("User not sent")

    regex = "([a-zA-Z0-9]){24}"
    not_valid_user_id = str(re.search(regex,user_id)) is None

    if (not_valid_user_id):
        return func.HTTPResponse("No user id found", status_codes=404)

    headers = {"Content-Type":"x-www-form-urlencoded"}

    if (code is not None): 
        data = {
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': REDIRECT_URI,
                'scope': 'identify email connections'
            }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    else:
        return func.HttpResponse("No code was sent")

    response = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers).json()

    if response.get('access_token') is None:
        return func.HttpResponse("Could not get access token")

    headers = {
        'Authorization': 'Bearer ' + str(response.get('access_token'))
        }
    
    response = requests.post('http://discordapp.com/api/users/@me', headers = headers).json()
    discord_user_id = int(response.get('id'))
    discord_username = str(response.get('username'))

    if discord_user_id is None or discord_username is None :
        return func.HttpResponse("Could not get user information")

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
        query = '''UPDATE users
                   SET discord_user_id = %s, discord_username = '%s'
                   WHERE user_id = '%s' '''  % (discord_user_id, discord_username, user_id)
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