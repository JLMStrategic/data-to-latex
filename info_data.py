""" The info_data.py script reads json files and uses the resume data inside said files
    to run the create_file() function from inject_tex.py insert data onto the resume. """

import json
import os
import re
from pprint import pprint
from inject_tex import create_file


JSON_DIR = './json'
JLM_RES_DIR = './jlmres'
JSON_FILES = [f for f in os.listdir(JSON_DIR) if os.path.isfile(os.path.join(JSON_DIR, f))]

def filter_alphanumeric(given):
    """ removes any character that is not a-z A-Z 0-9 space or () from the given string """
    regex = re.compile('[^a-zA-Z0-9() ]')
    result = regex.sub('', given)
    return result

def spec_chars(given):
    """ replace # or & with "number" or "and" respectively """
    no_ch = {'#':'number', '&':'and', '%':'\%', '\r\n•':'.', '\r\n':' ','\r':'', '\t':' ', '\n':'', '*':'', '•':''}
    for (key,value) in no_ch.items():
        if given and key in given:
            given = given.replace(key, value)

    return given

def check_exist(prefix, key_list):
    """ checks if the any of the keys used are found on the json string. if they aren't found,
    default to 'none' """

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
    test = spec_chars(test)
    return test

# fill_school function
#     useful: section of the json object that would be needed to use
def fill_school(useful):
    """ returns array of items that is needed to be injected """

    school_list = []
    school_sec = check_exist(useful, ['EducationHistory', 'SchoolOrInstitution'])

    for school in school_sec:
        school_name = check_exist(school, ['School', 'SchoolName'])
        school_start = check_exist(school, ['Degree', 'DatesOfAttendance', 'StartDate', 'YearMonth'])
        school_end = check_exist(school, ['Degree', 'DatesOfAttendance', 'EndDate', 'YearMonth'])
        school_degree = check_exist(school, ['Degree', 'DegreeName'])
        school_list.append([school_name, school_start, school_end, school_degree])

    return school_list

# fill_jobs function
#     useful: section of the json object that would be needed to use
def fill_jobs(useful):
    """ returns array of items that is needed to be injected """

    job_list = []
    job_sec = useful['EmploymentHistory']['EmployerOrg']
    for job in job_sec:
        job_info = job['PositionHistory'][0]
        job_org = check_exist(job_info, ['OrgName', 'OrganizationName'])
        job_start = check_exist(job_info, ['StartDate', 'YearMonth'])
        job_end = check_exist(job_info, ['EndDate', 'YearMonth'])
        job_title = check_exist(job_info, ['Title'])
        # job_description = useful['EmploymentHistory']['EmployerOrg'][0]['PositionHistory'][0]['Description']
        # job_description = check_exist(job_info, ['PositionHistory'])
        job_description = check_exist(job_info, ['Description'])
        print(job_description)

        job_list.append([job_org, job_start, job_end, job_title, job_description])

    return job_list

# fill_skills function
#     useful: section of the json object that would be needed to use
def fill_skills(useful):
    """ fills out the skill array based on candidate's qualifications summary """
    skills_sec = useful['Qualifications']['QualificationSummary'].replace('\r\n', ' --')
    skills = spec_chars(skills_sec).split(' --')
    skills = [s.strip() for s in [s for s in skills if s] if 'skills' not in s.lower()]
    skill_list = []

    # splits array into two-tuples
    while len(skills) > 2:
        split = skills[:2]
        skill_list.append(split)
        skills = skills[2:]
    skill_list.append(skills)
    if len(skill_list[-1]) == 1:
        skill_list[-1].append('')

    return skill_list

def main():
    """ Testing goes here. Split these for loops into functions in the future. """
    for file in JSON_FILES:
        with open(JSON_DIR + '/' + file, encoding='utf8') as json_file:
            data = json.load(json_file)

        useful = data['Resume']['StructuredXMLResume']

        person_name = check_exist(useful, ['ContactInfo', 'PersonName', 'GivenName']) + ' ' +\
                    check_exist(useful, ['ContactInfo', 'PersonName', 'FamilyName'])

        skill_list = fill_skills(useful)
        school_list = fill_school(useful)
        job_list = fill_jobs(useful)

        file_name = person_name.replace(' ', '-') + '-JLM'
        create_file(file_name, person_name, skill_list, job_list, school_list)

main()