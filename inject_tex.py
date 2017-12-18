""" The inject_tex.py script allows TeX code to be injected onto a template of the JLM Resume
    in LaTeX format. Then, the script will run pdflatex on all the new .tex files created. """

import os

CWD = os.getcwd()
THIS_FILE = __file__
RESUME_FOLDER = '/jlmres'
DUMP_FOLDER = '/dump'

# make new resumes go into jlmres folder, create folder if it does not exist
if not os.path.isdir(CWD + RESUME_FOLDER):
    os.makedirs(CWD + RESUME_FOLDER)
OUT_DIR = '.' + RESUME_FOLDER + '/'

if not os.path.isdir(CWD + RESUME_FOLDER):
    os.makedirs(CWD + DUMP_FOLDER)
DUMP_DIR = '.' + DUMP_FOLDER + '/'

# Search for this exact string on TeX file to know
# which line to append to
NAME_TEXT = '% NAME CODE HERE'
SKILL_TEXT = '% SKILLS CODE HERE'
WORK_TEXT = '% EXP CODE HERE'
EDU_TEXT = '% EDU CODE HERE'

with open(CWD + '/JLM_Resume.tex', 'r', encoding='utf8') as f:
    READ = f.readlines()


# add_name function
#     name: person's full name {first, middle, last} as a string
def add_name(read_data, name_line, name):
    """ Adds skill1 and skill2 onto the skills section of the TeX file. """


    new_name = '\\Huge{{{}}}'.format(name)
    read_data[name_line] = read_data[name_line].strip() + new_name

    print("Added name: {}".format(name))


# add_skill function
#     skill1: skill to appear on left side
#     skill2: skill to appear on right side
#     end: last skills bullets will not have extra padding. default=False
def add_skill(read_data, skill_line, skill1, skill2, end=False):
    """ Adds skill1 and skill2 onto the skills section of the TeX file. """

    add_line = '\\skillItem{{{}}}{{{}}}\n'.format(skill1, skill2)

    # considers odd number of skill bullet points
    if not skill2:
        add_line_end = '\\skillOneItemEnd{{{}}}'.format(skill1)
    else:
        add_line_end = '\\skillItemEnd{{{}}}{{{}}}\n'.format(skill1, skill2)

    # inject add_line one the SKILL_LINE on TeX doc
    if end:
        read_data[skill_line] = read_data[skill_line].strip() + add_line_end
    else:
        read_data[skill_line] = read_data[skill_line].strip() + add_line

    print("Added {} and {} as new row of skills".format(skill1, skill2))


#  add_work_exp function
#     company: name of the company
#     start_date: date started working
#     end_date: date ended working
#     position: job title
#     desc: list of descriptions for this specific job
def add_work_exp(read_data, work_line, company, start_date, end_date, position, desc):
    """ Creates new work experience subsection. """

    new_work = '\\newWorkExp{{{}}}{{{}}}{{{}}}{{{}}}'.format(
        company, start_date, end_date, position)
    work_sec_start = '\\workExpStart'
    work_sec_end = '\\workExpEnd'
    desc_items = ''

    for item in desc:
        desc_items += add_work_desc(item)

    # inject new_work block onto TeX file
    if desc:
        read_data[work_line] = read_data[work_line].strip() +\
                            new_work + work_sec_start + desc_items + work_sec_end
    else:
        read_data[work_line] = read_data[work_line].strip() + new_work
    print("Added {} job experience to resume".format(company))


# add_work_desc function
#     description: description bullet point
#     last: last bullet point needs specific formatting
def add_work_desc(description):
    """ Adds a new buillet point onto the description section of work experience. """

    new_desc = '\\workExpItem{{{}}}'.format(description)
    return new_desc


# add_edu function
#     school: previous school name
#     start_date: enrollment date
#     end_date: graduation date
#     degree: degree
def add_edu(read_data, edu_line, school, start_date, end_date, degree):
    """ Adds education information onto its section. """

    new_edu = '\\newEducation{{{}}}{{{}}}{{{}}}{{{}}}'.format(school, start_date, end_date, degree)
    read_data[edu_line] = read_data[edu_line].strip() + new_edu

    print("Added {} to resume".format(school))


# create_file function
#     filename: name of the pdf file they wish to receive
#               does not require file extension or path
#     fullname: name of the person's resume
#     skill_list: list of all skills they contain
#           ex. [[skill1, skill2], [skill3, skill4]]
#     work_list: list of all previous jobs with nested descriptions list
#           ex. [[company, start, end, position, [desc1, desc2]]]
#     edu_list: list of all previous education
#           ex. [[school1, start, end, degree], [school2, start, end, degree]]
def create_file(filename, fullname, skill_list, work_list, edu_list):
    """ TeX file creation function. incorporates all add_*() functions """

    read_data = list(READ)
    input_lines = find_lines(read_data)

    add_name(read_data, input_lines['NameLine'], fullname)

    # odd skill lists should have "" as the last skill
    last_skill = skill_list[-1] if skill_list else []
    for skill in skill_list:
        if not last_skill:
            break
        if skill == last_skill:
            add_skill(read_data, input_lines['SkillLine'], skill[0], skill[1], end=True)
        else:
            add_skill(read_data, input_lines['SkillLine'], skill[0], skill[1])
    for work in work_list:
        if work_list:
            add_work_exp(read_data, input_lines['WorkLine'],
                         work[0], work[1], work[2], work[3], work[4])
    for edu in edu_list:
        if edu_list:
            add_edu(read_data, input_lines['EduLine'], edu[0], edu[1], edu[2], edu[3])

    # writes all changes to file
    with open(DUMP_DIR + filename + '.tex', 'w+', encoding='utf8') as file_w:
        file_w.writelines(read_data)
    print("Created new {}.tex file".format(filename))

    print("Running pdflatex to compile {}.tex to pdf".format(filename))
    run_pdf(filename)


# find_lines
#     read_data: file list after using open()
def find_lines(read_data):
    """ changes where the injection lines would be found """

    result = {'NameLine': -1, 'SkillLine': -1, 'WorkLine': -1, 'EduLine': -1}

    # line search
    for index, value in enumerate(read_data):
        item = value.strip()
        if item == NAME_TEXT and result['NameLine'] == -1:
            result['NameLine'] = index + 1
            index = 0

        if item == SKILL_TEXT and result['SkillLine'] == -1:
            result['SkillLine'] = index + 1
            index = 0

        if item == WORK_TEXT and result['WorkLine'] == -1:
            result['WorkLine'] = index + 1
            index = 0

        if item == EDU_TEXT and result['EduLine'] == -1:
            result['EduLine'] = index + 1
            index = 0

    print(result)
    return result

# run_pdf
#     filename: name of the tex file, does not need the .tex extension
def run_pdf(filename):
    """ runs the command pdflatex with the given tex file then places pdfs
    to the res folder and other files onto a dump folder """

    full_file = DUMP_DIR + filename + '.tex'
    # pdf_folder = '.' + OUT_DIR
    os.system('pdflatex --output-directory={} {}'.format(DUMP_DIR, full_file))
    os.system('mv {}/*.pdf {}'.format(DUMP_DIR, OUT_DIR))
