import requests
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
    return token

    
getToken()