import requests
import datetime
import os.path
from getpass import getpass
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
def assetCount():
    refreshToken()
    # Get the token
    token = getToken()

    url = 'https://gateway.qg1.apps.qualys.com/am/v1/assets/host/count'

    headers = {'Authorization' : 'Bearer ' + token}

    # Make the request and get count of assets
    request = requests.post(url = url, headers = headers)

    response = eval(formatResponse(request))
    return response['count']
    

# Gets details of all assets
def assetDetails():
    refreshToken()
    # Get token.
    token = getToken()

    url = "https://gateway.qg1.apps.qualys.com/am/v1/assets/host/list"

    headers = {
        'Authorization' : 'Bearer ' + token,
    }

    # Make the request
    request = requests.post(url = url, headers = headers)
    response = formatResponse(request)

    print(response, file=open("assetDetails.json", "w"))


assetDetails()
