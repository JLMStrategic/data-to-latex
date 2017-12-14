import json
import os
from pprint import pprint
from inject_tex import create_file


JSON_DIR = './json'
JLM_RES_DIR = './jlmres'
json_files = [f for f in os.listdir(JSON_DIR) if os.path.isfile(os.path.join(JSON_DIR, f))]


def check_exist(prefix, key_list):
    test = ''
    dummy = []
    for key in key_list:
        try:
            dummy.append(prefix[key])
        except:
            return 'none'

        if test == '':
            prefix = prefix[key]

    test = prefix
    if isinstance(test, list):
        return test
    no_ch = ['#', '&']
    for ch in no_ch:
        if test and ch in test:
            test = test.replace(ch, '\\' + ch)
    return test.replace('!#$^&*', 'n') if test else test


def main():
    for file in json_files:
        with open(JSON_DIR + '/' + file, encoding='utf8') as json_file:
            data = json.load(json_file)

        useful = data['Resume']['StructuredXMLResume']

        person_name = check_exist(useful, ['ContactInfo', 'PersonName', 'GivenName']) + ' ' +\
                    check_exist(useful, ['ContactInfo', 'PersonName', 'FamilyName'])

        school_list = []
        school_sec = check_exist(useful, ['EducationHistory', 'SchoolOrInstitution'])

        for school in school_sec:
            school_name = check_exist(school, ['School', 'SchoolName'])
            school_start = check_exist(school,
                        ['Degree', 'DatesOfAttendance', 'StartDate', 'YearMonth'])
            school_end = check_exist(school,
                        ['Degree', 'DatesOfAttendance', 'EndDate', 'YearMonth'])
            school_degree = check_exist(school, ['Degree', 'DegreeName'])
            school_list.append([school_name, school_start, school_end, school_degree])

        job_list = []
        job_sec = useful['EmploymentHistory']['EmployerOrg']
        for job in job_sec:
            job_info = job['PositionHistory'][0]
            job_org = check_exist(job_info, ['OrgName', 'OrganizationName'])
            job_start = check_exist(job_info, ['StartDate', 'YearMonth'])
            job_end = check_exist(job_info, ['EndDate', 'YearMonth'])
            job_title = check_exist(job_info, ['Title'])
            # job_description = useful['EmploymentHistory']['EmployerOrg']
            #                   [0]['PositionHistory'][0]['Description']
            job_description = []
            job_list.append([job_org, job_start, job_end, job_title, job_description])


        file_name = person_name.replace(' ', '-') + '-JLM'
        create_file(file_name, person_name, [], job_list, school_list)


main()