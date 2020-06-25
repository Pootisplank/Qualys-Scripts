import xml.etree.ElementTree as ET


reportName = "Alex *Global* GISG VM KRI (Asset tags) BU-All (3-5)"
file = 'reportList.xml'
tree = ET.parse(file)
root = tree.getroot()



# for child in root:
#     for child1 in child:
#         print(child1.tag, child1.attrib)

# Find the first report with title reportName and print the report ID
for report in root.find("RESPONSE").find("REPORT_LIST").findall("REPORT"):
    if report.find("TITLE").text == "Alex *Global* GISG VM KRI (Asset tags) BU-All (3-5)":
        print(report.find("ID").text)