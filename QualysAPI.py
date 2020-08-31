import xml.etree.ElementTree as ET
import requests
from getpass import getpass
import os
from datetime import datetime

# Reads a file called cred_ini on the Desktop to obtain username, password, and location to save files.
# cred_ini formatting: Username in first line, password in second line, save location in third line.
# Return: The data as a python dictionary
def getCred():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\Qualys_Cred')
    ini = 'cred_ini'
    cred = os.path.join(desktop, ini)
    
    with open(cred, 'r') as file:
      username = file.readline().strip('\n')
      password = file.readline().strip('\n')
      save = file.readline().strip('\n')
    return {
      'username' : username,
      'password' : password,
      'save' : save
    }
    
def formatResponse(response):
  # Reformats the response
  #responseFormatted = str(response.content)
  #responseFormatted = responseFormatted.replace('\\n', '\n')
  #responseFormatted = responseFormatted[2:-1]
  responseFormatted = response.content.decode('utf-8')
  return responseFormatted


def login():
  creds = getCred()
  username = creds['username']
  password = creds['password']
  save = os.path.join(creds['save'], 'outputLogin.xml')
  
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
  print(responseFormatted, file=open(save,"w"))
  return session


def logout(session):
  creds = getCred()
  save = os.path.join(creds['save'], 'outputLogout.xml')
  
  url = "https://qualysapi.qualys.com/api/2.0/fo/session/"
  payload = {'action': 'logout'}  
  headers = {
    'X-Requested-With': 'PyRequests',
  }

  # Makes request
  response = session.post(url, headers = headers, params = payload)

  # Reformat and save response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open(save,"w"))


def getHost(session):
  creds = getCred()
  save = os.path.join(creds['save'], 'hostList.xml')
  
  url = "https://qualysapi.qualys.com/api/2.0/fo/asset/host/"
  payload = {'action':'list'}
  headers = {
    'X-Requested-With': 'PyRequests',
  }
  # Makes the request
  response = session.get(url, headers=headers, params = payload)

  # Reformat and save response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open(save,"w"))


def getReportList(session):
  creds = getCred()
  save = os.path.join(creds['save'], 'reportList.xml')
  
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
  print(responseFormatted, file=open(save,"w"))


def getReportTemplates(session):
  creds = getCred()
  save = os.path.join(creds['save'], 'reportTemplates.xml')
  
  url = "https://qualysapi.qualys.com/msp/report_template_list.php"
  headers = {
    'X-Requested-With': 'PyRequests',
  }
  # Makes the request
  response = session.get(url, headers = headers)
  
  # Reformat and save response
  responseFormatted = formatResponse(response)
  print(responseFormatted, file=open(save,"w"))


def launchScoreCard(session, name):
  creds = getCred()
  save = os.path.join(creds['save'], 'launchScoreCard.xml')
  
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
  print(responseFormatted, file=open(save,"w"))


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
  creds = getCred()
  save = os.path.join(creds['save'], 'downloadReport.xml')
  
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
  print(responseFormatted, file=open(save,"w"))


def collect_appliances(session):
  creds = getCred()
  dt = str(datetime.utc.now()).replace(' ', '__').replace(':','_').replace('.','_')
  filename = 'collectAppliances_{0}.xml'.format(dt)
  save = os.path.join(creds['save'], filename)

  
  url = "https://qualysapi.qualys.com/api/2.0/fo/compliance/control"
    
  payload = {
    'action' : 'list',
    'details' : 'Basic',
    'truncation_limit': '1000000'
  }
    
  headers = {
    'X-Requested-With': 'PyRequests'
  }
  response = session.post(url = url, headers = headers, data = payload)
  responseFormatted = response.content.encode('utf-8')
  print(responseFormatted, file=open(save, 'w'))

