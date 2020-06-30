import requests
from getpass import getpass
from GetReports import formatResponse


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

    headers = {"ContentType" : "application/x-www-form-urlencoded"}

    request = requests.post(url = url, params = payload, headers = headers)

    responseFormatted = formatResponse(request)
    print(responseFormatted, file=open("token.xml","w"))
    print("Getting Token")


getToken()