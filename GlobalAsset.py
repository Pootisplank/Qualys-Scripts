# Import Standard Library 
import time
from datetime import datetime
from sys import exit
import os
import json
from getpass import getpass

import requests
from QualysAPI import formatResponse, getCred


# Generates a token that expires in 4 hours.
def generateToken():
    creds = getCred()
    username = creds['username']
    password = creds['password']

    url = 'https://gateway.qg1.apps.qualys.com/auth/'

    payload = {
        'username' : username, 
        'password' : password,
        'token' : 'true'
    }

    headers = {
        'ContentType' : 'application/x-www-form-urlencoded',
    }

    request = requests.post(url = url, data = payload, headers = headers)

    token = formatResponse(request)
    print('Token receieved, login successful.')
    print(token, file=open('token.txt', 'w'))
    print(datetime.now(), file=open('token.txt', 'a'))
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
    token_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    current_time = datetime.now()
    time_difference = (current_time - token_time).total_seconds() / 3600

    # If the token was generated four hours or later ago, get a new token.
    if (time_difference >= 4):
        print('Token Expired, please login again.')
        generateToken()
        

# Gets the token from token.txt and returns it.
def getToken():
    with open('token.txt', 'r') as file:
        token = file.readline().strip('\n')
    return token


def mergeJson(json_list, lastSeenAssetId, has_more):
    master_internet_facing = json_list[0]
    master_internet_facing['lastSeenAssetId'] = lastSeenAssetId
    for index in range(1, len(json_list)):
        master_internet_facing['count'] += json_list[index]['count']
        assetListData = json_list[index]['assetListData']['asset']
                
        for data in assetListData:
            master_internet_facing['assetListData']['asset'].append(data)
    master_internet_facing['hasMore'] = has_more       
    return master_internet_facing 
        

def internetFacingCount():
    refreshToken()
    token = getToken()
    url = 'https://gateway.qg1.apps.qualys.com/am/v1/assets/host/filter/list'

    # Initialize variables
    pages = 1
    time_msg = ''        
    last_seen_id = '0'
    has_more = 1
    final_count = 0
    api_rest_time = 0
    if_json_list = []
    current_time = datetime.now().strftime('%b-%d-%y %H-%M-%S')

    headers = {
        'Authorization' : 'Bearer ' + token,
    }
            
    payload = {
        'lastSeenAssetId' : last_seen_id,
        'includeFields' : 'tag',
        #'filter' : 'tags.name:TMCC - AK-Windows Assets'
        #'filter' : 'tags.name:BU~*'
        #'filter' : 'tags.name:"OI: Disk Full"'
    }
    
    creds = getCred()
    dt = str(datetime.utc.now().date())
    filename = 'internetFacing_{0}.xml'.format(dt)
    save = os.path.join(creds['save'], filename)

    # Check log folder
    if (not(os.path.exists('logs'))):
        os.makedirs('logs')
        os.makedirs('./logs/error')
    elif (not(os.path.exists('./logs/error'))):
        os.makedirs('./logs/error')
        
    # Check if we are extending a report
    extend_report = os.path.isfile('internetFacing.json')
    if (extend_report):
        with open('internetFacing.json') as file:
            if_json_list.append(json.load(file))
        if (if_json_list[0]['hasMore'] == 0):
            print("Report already finished.  Exiting program.")
            exit()
        payload['lastSeenAssetId'] = if_json_list[0]['lastSeenAssetId']

    # Request host details and save them as json
    while (has_more != 0):
        # Record time for logging
        start_time = time.time()
        
        # Get token
        refreshToken()
        token = getToken()

        # Make the request
        request = requests.post(url = url, headers = headers, data = payload)
        response = formatResponse(request)
            
        # Check for request error
        if (request.status_code != 200):
            time_msg += ('Page %s (Crash) - %s seconds\n' % (pages, time.time() - start_time))
            error_msg = 'Error: Status Code ' + f'{request.status_code}. Read ' + f'{pages-1}' + ' pages. Exiting program.\n' + time_msg
            print(error_msg)   
            
            # Save error log
            with open(f'./logs/error/{current_time}', 'w') as file:
                file.write(error_msg)
                
            if (pages == 1):
                exit()
                
           # Save report progress
            master_internet_facing = mergeJson(if_json_list, payload['lastSeenAssetId'], has_more)
            
            # Save the final report
            with open('internetFacing.json', 'w') as file:
                json.dump(master_internet_facing, file, indent=4)               
             
            exit()
                       
        # Create a json object from the response and add it to the list.
        asset_json = json.loads(response)
        if_json_list.append(asset_json)
                          
        # Update last_seen_id
        payload['lastSeenAssetId'] = asset_json['lastSeenAssetId']
        
        final_count += asset_json['count']
            
        # Update has_more
        has_more = asset_json['hasMore']
        
        time_msg += ('Page %s - %s seconds\n' % (pages, time.time() - start_time))
        
        pages += 1
    
    # Merge all reports in the list of json objects.
    master_internet_facing = mergeJson(if_json_list, payload['lastSeenAssetId'], has_more)
    
    # Save the final report
    with open('internetFacing.json', 'w') as file:
        json.dump(master_internet_facing, file, indent=4)

    # Save logs
    with open(f'./logs/{current_time}', 'w') as file:
        file.write(time_msg)        
        
    return final_count
        
        
print(internetFacingCount())
