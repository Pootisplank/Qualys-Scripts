import QualysAPI

session = QualysAPI.login()
QualysAPI.getHost(session)
QualysAPI.logout(session)

