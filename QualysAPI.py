import xml.etree.ElementTree as ET
import requests
from getpass import getpass



def formatResponse(response):
  # Reformats the response
  #responseFormatted = str(response.content)
  #responseFormatted = responseFormatted.replace('\\n', '\n')
  #responseFormatted = responseFormatted[2:-1]
  responseFormatted = response.content.decode('utf-8')
  return responseFormatted


def login():
  username = input("Enter a username: ")
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

  # Makes request
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
  # Makes the request
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

  # Makes the request
  response = session.get(url, headers = headers, params = params)
  
  # Reformat and save response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open("reportList.xml","w"))


def getReportTemplates(session):
  url = "https://qualysapi.qualys.com/msp/report_template_list.php"
  headers = {
    'X-Requested-With': 'PyRequests',
  }
  # Makes the request
  response = session.get(url, headers = headers)
  
  # Reformat and save response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open("reportTemplates.xml","w"))


def launchScoreCard(session, name):
  url = "https://qualysapi.qualys.com/api/2.0/fo/report/scorecard/"
  headers = {
    'X-Requested-With': 'PyRequests',
  }
  params = {
    'action' : 'launch',
    'name' : name,
    'output_format' : 'xml'
  }

  # Makes the request
  response = session.post(url, headers = headers, data = params)

  # Reformat and save response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open("launchScoreCard.xml","w"))


def findReportID(session, reportName):
  file = 'reportList.xml'

  # Parse xml file
  tree = ET.parse(file)
  root = tree.getroot()

  # Find the first report with title reportName and print the report ID
  for report in root.find("RESPONSE").find("REPORT_LIST").findall("REPORT"):
      if report.find("TITLE").text == reportName:
          return report.find("ID").text


def downloadReport(session, reportID):
  url = "https://qualysapi.qualys.com/api/2.0/fo/report/"
  headers = {
    'X-Requested-With': 'PyRequests',
  }
  params = {
    'action' : 'fetch',
    'id' : reportID
  }

  response = session.post(url = url, headers = headers, params = params)
  # Reformat and save response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open("downloadReport.xml","w"))

