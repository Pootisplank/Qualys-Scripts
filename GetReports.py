from QualysAPI import *

# Logs in with username/password, downloads report list, runs/downloads a report of your choice.

session = login()
getHost(session)
getReportTemplates(session) # Access denied at the moment
launchScoreCard(session, "Alex *Global* GISG VM KRI (Asset tags) BU-All (3-5)")
getReportList(session)
reportID = findReportID(session, "Alex *Global* GISG VM KRI (Asset tags) BU-All (3-5)")
downloadReport(session, reportID)
logout(session)