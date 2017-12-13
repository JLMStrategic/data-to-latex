import json
from pprint import pprint

JSON_DIR = './json'

with open(JSON_DIR + '/' + 'Angie_Yuan.json') as json_file:
    data = json.load(json_file)

# pprint(data)
# print(data)

# pprint(data['Resume'].keys())
# pprint(data['Resume']['NonXMLResume'].keys())

# pprint(data['Resume']['StructuredXMLResume'].keys())

# How to get Name
# print(data['Resume']['StructuredXMLResume']['ContactInfo']['PersonName']['FormattedName'])

# How to get School Info
# print(data['Resume']['StructuredXMLResume']['EducationHistory']['SchoolOrInstitution'][0]['School']['SchoolName'])
# print(data['Resume']['StructuredXMLResume']['EducationHistory']['SchoolOrInstitution'][0]['Degree']['DatesOfAttendance']['StartDate']['YearMonth'])
# print(data['Resume']['StructuredXMLResume']['EducationHistory']['SchoolOrInstitution'][0]['Degree']['DatesOfAttendance']['EndDate']['YearMonth'])
# print(data['Resume']['StructuredXMLResume']['EducationHistory']['SchoolOrInstitution'][0]['Degree']['DegreeName'])

# How to get Job Info
# print(data['Resume']['StructuredXMLResume']['EmploymentHistory']['EmployerOrg'][0]['EmployerOrgName'])
# print(data['Resume']['StructuredXMLResume']['EmploymentHistory']['EmployerOrg'][0]['PositionHistory'][0]['StartDate']['YearMonth'])
# print(data['Resume']['StructuredXMLResume']['EmploymentHistory']['EmployerOrg'][0]['PositionHistory'][0]['EndDate']['YearMonth'])
# print(data['Resume']['StructuredXMLResume']['EmploymentHistory']['EmployerOrg'][0]['PositionHistory'][0]['Title'])
# print(data['Resume']['StructuredXMLResume']['EmploymentHistory']['EmployerOrg'][0]['PositionHistory'][0]['Description'])

# TODO: How to reformat skills into short words or sentences
# print(data['Resume']['StructuredXMLResume']['Qualifications']['QualificationSummary'])

