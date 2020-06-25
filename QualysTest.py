import requests
from getpass import getpass

def formatResponse(response):
  # Reformats the response
  responseFormatted = str(response.content)
  responseFormatted = responseFormatted.replace('\\n', '\n')
  responseFormatted = responseFormatted[2:-1]
  return responseFormatted


def login():
  username = input("Enter username: ")
  password = getpass()

  url = "https://qualysapi.qualys.com/api/2.0/fo/session/"
  # Query Params
  payload = {
    'action' : 'login', 
    'username' : username, 
    'password' : password
  }
  # Headers
  headers = {
    'X-Requested-With' : 'PyRequests'
  }

  # Make the login request
  session = requests.Session()
  response = session.post(url, headers = headers, params = payload)

  # Reformats the response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open("outputLogin.xml","w"))
  return session


def logout(session):
  url = "https://qualysapi.qualys.com/api/2.0/fo/session/"
  payload = {'action': 'logout'}
  headers = {
    'X-Requested-With': 'PyRequests',
  }

  # Makes request and stores response
  response = session.post(url, headers = headers, params = payload)

  # Reformat and save response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open("outputLogout.xml","w"))


def getHost(session):
  url = "https://qualysapi.qualys.com/api/2.0/fo/asset/host/"
  payload = {'action':'list'}
  headers = {
    'X-Requested-With': 'PyRequests',
  }
  # Makes the request and stores response
  response = session.get(url, headers=headers, params = payload)

  # Reformat and save response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open("hostList.xml","w"))


def getReportList(session):
  url = "https://qualysapi.qualys.com/api/2.0/fo/report/"
  params = {'action' : 'list'}
  data = {'Content-Type': 'text/xml'}
  files = []
  headers = {
    'X-Requested-With' : 'PyRequests',
    'Content-Type' : 'text/xml'
  }

  # Makes the request and stores the response
  response = session.get(url, headers = headers, params = params)
  
  # Reformat and save response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open("reportList.xml","w"))



session = login()
getHost(session)
getReportList(session)
logout(session)