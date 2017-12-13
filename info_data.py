import json
from pprint import pprint
from inject_tex import create_file

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

JSON_DIR = './json'

with open(JSON_DIR + '/' + 'Angie_Yuan.json') as json_file:
    data = json.load(json_file)

useful = data['Resume']['StructuredXMLResume']


person_name = str(useful['ContactInfo']['PersonName']['FormattedName'])

school_list = []
school_sec = useful['EducationHistory']['SchoolOrInstitution']
for school in school_sec:
    school_name = str(school['School']['SchoolName'])
    school_start = str(school['Degree']['DatesOfAttendance']['StartDate']['YearMonth'])
    school_end = str(school['Degree']['DatesOfAttendance']['EndDate']['YearMonth'])
    school_degree = str(school['Degree']['DegreeName'])
    school_list.append([school_name, school_start, school_end, school_degree])

job_list = []
job_sec = useful['EmploymentHistory']['EmployerOrg']
for job in job_sec:
    job_info = job['PositionHistory'][0]
    job_org = str(job_info['OrgName']['OrganizationName'])
    job_start = str(job_info['StartDate']['YearMonth'])
    job_end = str(job_info['EndDate']['YearMonth'])
    job_title = str(job_info['Title'])
    # job_description = useful['EmploymentHistory']['EmployerOrg'][0]['PositionHistory'][0]['Description']
    job_description = []
    job_list.append([job_org, job_start, job_end, job_title, job_description])


file_name = person_name.replace(' ', '-') + '_JLM'
create_file(file_name, person_name, [], job_list, school_list)
