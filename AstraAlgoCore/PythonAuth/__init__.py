import logging
import json
import azure.functions as func
import os
import requests

# GET ACCESS TOKEN FUNCTION
#
# CALLED FROM:  Create Order and Get User Dashboard functions
#
# FUNCTION:     This Function is used to get an Access Token from an existing non expired Refresh Token
#
# PARAMS:       header - <refresh_token> : Used to be passed into the td ameritrade token auth endpoint to get a new access token
#
# RESPONSE:     Returns the access_token in the header

def main(req: func.HttpRequest) -> func.HttpResponse:
    payload = None
    refresh_token = req.headers.get('refresh_token')
    headers = { "Content-Type":"application/x-www-form-urlencoded" }
    
    # If the user sent in a refresh token then send the refresh token in the payload
    if (refresh_token is not None):
        payload = { 
            'grant_type': 'refresh_token', 
            'refresh_token': refresh_token, 
            'client_id': os.environ["API_KEY"],
            'redirect_uri': " https://localhost:44352/account/td"
            }
    else:
        return func.HttpResponse("No token was sent")

    user_authentication_data = requests.post(r'https://api.tdameritrade.com/v1/oauth2/token', headers = headers, data=payload)
    
    decoded_content = user_authentication_data.json()

    if(decoded_content.get('error') is not None):
        return func.HttpResponse(str(decoded_content.get('error')))

    elif (decoded_content.get('access_token') is not None):
        access_token = { 'access_token': decoded_content['access_token'] }
        return func.HttpResponse(headers=access_token)