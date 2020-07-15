from time import sleep
import datetime
import os.path
import json
from getpass import getpass

import requests
from QualysAPI import formatResponse


# Generates a token that expires in 4 hours.
def generateToken():
    username = input("Enter the username: ")
    password = getpass()

    url = "https://gateway.qg1.apps.qualys.com/auth/"

    payload = {
        'username' : username, 
        'password' : password,
        'token' : 'true'
    }

    headers = {
        "ContentType" : "application/x-www-form-urlencoded",
    }

    request = requests.post(url = url, data = payload, headers = headers)

    token = formatResponse(request)
    print("Token receieved, login successful.")
    print(token, file=open("token.txt", "w"))
    print(datetime.datetime.now(), file=open("token.txt", "a"))
    return token


# Checks if token has expired.  If so, generates a new token.
def refreshToken():
    # If token record does not exist, regenerate token.
    if (not(os.path.isfile('token.txt'))):
        generateToken()
        return

    # Gets when the token was generated.
    with open('token.txt', 'r') as file:
        file.readline()
        date = file.readline().strip('\n')

    # Computes how much time as passed since token was generated.
    token_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    current_time = datetime.datetime.now()
    time_difference = (current_time - token_time).total_seconds() / 3600

    # If the token was generated four hours or later ago, get a new token.
    if (time_difference >= 4):
        print("Token Expired, please login again.")
        generateToken()
        


# Gets the token from token.txt and returns it.
def getToken():
    with open('token.txt', 'r') as file:
        token = file.readline().strip('\n')
    return token


# Returns the total number of assets
def assetCount(last_seen_id):
    refreshToken()
    # Get the token
    token = getToken()

    url = 'https://gateway.qg1.apps.qualys.com/am/v1/assets/host/count'

    headers = {
        'Authorization' : 'Bearer ' + token,
        'lastSeenID' : last_seen_id
    }

    # Make the request and get count of assets
    request = requests.post(url = url, headers = headers)

    response = eval(formatResponse(request))
    return response['count']
    

# Gets details of all assets
def assetDetails():
    refreshToken()
    token = getToken()
    url = "https://gateway.qg1.apps.qualys.com/am/v1/assets/host/list"
    
    last_seen_id = "0"
    has_more = 1

    headers = {
        'Authorization' : 'Bearer ' + token,
        'includeFields' : 'agentID'
    }
    
    payload = {
        'lastSeenAssetId' : last_seen_id,
    }
    
    asset_json_list = []

    i = 0
    # Get all asset information in a list of json objects.
    while (i < 5):
        # Get token
        refreshToken()
        token = getToken()

        # Make the request
        request = requests.post(url = url, headers = headers, data = payload)
        response = formatResponse(request)

        # Create a json object from the response and add it to the list of reports.
        asset_json = json.loads(response)
        asset_json_list.append(asset_json)
                
        # Update last_seen_id
        last_seen_id = asset_json['lastSeenAssetId']
        payload['lastSeenAssetId'] = f"{last_seen_id}"
        
        # Update has_more
        has_more = asset_json["hasMore"]
        i = i + 1
        
        
    # Initialize the final json report as the first json in the list.
    master_asset_details = asset_json_list[0]
    
    # Update the lastSeenAssetID in the final report.
    master_asset_details["lastSeenAssetId"] = asset_json_list[len(asset_json_list) - 1]["lastSeenAssetId"]
    
    # Merge all reports in the list of json objects.
    for index in range(1, len(asset_json_list)):
        master_asset_details["count"] += asset_json_list[index]["count"]
        assetListData = asset_json_list[index]["assetListData"]["asset"]
        
        for data in assetListData:
            master_asset_details["assetListData"]["asset"].append(data)
        
    # Save the final report
    with open("assetDetails.json", "w") as file:
        json.dump(master_asset_details, file, indent=4)
        

def internetFacingCount():
    refreshToken()
    token = getToken()
    url = "https://gateway.qg1.apps.qualys.com/am/v1/assets/host/filter/list"
        
    last_seen_id = "0"
    has_more = 1
    final_count = 0

    headers = {
        'Authorization' : 'Bearer ' + token,
        'includeFields' : 'tag'
    }
        
    payload = {
        'lastSeenAssetId' : last_seen_id,
        'includeFields' : 'tag',
        'filter' : 'tags.name:BU~*'
    }

    i = 0
    while (has_more != 0):
        sleep(10)
        # Get token
        refreshToken()
        token = getToken()

        # Make the request
        request = requests.post(url = url, headers = headers, data = payload)
        response = formatResponse(request)

        # Create a json object from the response.
        asset_json = json.loads(response)
                          
        # Update last_seen_id
        payload['lastSeenAssetId'] = f"{asset_json['lastSeenAssetId']}"
        final_count += asset_json["count"]
            
        # Update has_more
        has_more = asset_json["hasMore"]
        i = i + 1
        
        # Save the final report
        # with open("assetDetails.json", "w") as file:
            # json.dump(asset_json, file, indent=4)
            
    return final_count
        
print(internetFacingCount())
