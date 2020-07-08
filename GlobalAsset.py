import requests
import datetime
from getpass import getpass
from QualysAPI import formatResponse


# Token expires in 4 hours
def getToken():
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
        "X-Requested-With" : "PyRequests"
    }

    request = requests.post(url = url, data = payload, headers = headers)

    token = formatResponse(request)
    print("Token receieved, login successful.")
    print(token, file=open("token.txt", "w"))
    print(datetime.datetime.now(), file=open("token.txt", "a"))
    return token


# Checks if token has expired.  If so, generates a new token.
def refreshToken():
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
        getToken()

    
#getToken()
refreshToken()