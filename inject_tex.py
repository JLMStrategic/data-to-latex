import os
import io

CWD = os.getcwd()
THIS_FILE = __file__
print(THIS_FILE)
RESUME_FOLDER = '/jlmres'

# make new resumes go into jlmres folder, create folder if it does not exist
if not os.path.isdir(CWD + RESUME_FOLDER):
    os.makedirs(CWD + RESUME_FOLDER)
OUT_DIR = '.' + RESUME_FOLDER + '/'


# Search for this exact string on TeX file to know
# which line to append to
NAME_TEXT = '% NAME CODE HERE'
SKILL_TEXT = '% SKILLS CODE HERE'
WORK_TEXT = '% EXP CODE HERE'
EDU_TEXT = '% EDU CODE HERE'

# Open the TeX file and store onto read_data list
with open(CWD + '/JLM_Resume.tex', 'r') as f:
    read_data = f.readlines()


# add_name function
#     adds skill1 and skill2 onto the skills section of the TeX file
#     name: person's full name {first, middle, last} as a string
def add_name(name_line, name):
    add_name = '\\Huge{{{}}}'.format(name)
    read_data[name_line] = read_data[name_line].strip() + add_name

    print("Added name: {}".format(name))


# add_skill function
#     adds skill1 and skill2 onto the skills section of the TeX file
#     skill1: skill to appear on left side
#     skill2: skill to appear on right side
#     end: last skills bullets will not have extra padding. default=False
def add_skill(skill_line, skill1, skill2, end=False):
    add_line = '\\skillItem{{{}}}{{{}}}\n'.format(skill1, skill2)
    add_line_end = '\\skillItemEnd{{{}}}{{{}}}\n'.format(skill1, skill2)

    # inject add_line one the SKILL_LINE on TeX doc
    if end:
        read_data[skill_line] = read_data[skill_line].strip() + add_line_end
    else:
        read_data[skill_line] = read_data[skill_line].strip() + add_line

    print("Added {} and {} as skill 1 and skill 2".format(skill1, skill2))


#  add_work_exp function
#     creates a new work experience section for the TeX file
#     company: name of the company
#     start_date: date started working
#     end_date: date ended working
#     position: job title
#     desc: list of descriptions for this specific job
def add_work_exp(work_line, company, start_date, end_date, position, desc):
    new_work = '\\newWorkExp{{{}}}{{{}}}{{{}}}{{{}}}'.format(
        company, start_date, end_date, position)
    work_sec_start = '\\workExpStart'
    work_sec_end = '\\workExpEnd'
    desc_items = ''

    for item in desc:
        desc_items += add_work_desc(item)

    # inject new_work block onto TeX file
    read_data[work_line] = read_data[work_line].strip() +\
                        new_work + work_sec_start + desc_items + work_sec_end

    print("Added {} job experience to resume".format(company))


# add_work_desc function
#     adds a new bullet point to the work experience section
#     description: description bullet point
#     last: last bullet point needs specific formatting
def add_work_desc(description):
    new_desc = '\\workExpItem{{{}}}'.format(description)
    return new_desc


# add_edu function
#     school: previous school name
#     start_date: enrollment date
#     end_date: graduation date
#     degree: degree
def add_edu(edu_line, school, start_date, end_date, degree):
    new_edu = '\\newEducation{{{}}}{{{}}}{{{}}}{{{}}}'.format(school, start_date, end_date, degree)
    read_data[edu_line] = read_data[edu_line].strip() + new_edu

    print("Added {} to resume".format(school))


# create_file function
#     TeX file creation function. incorporates all add_*() functions
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
    input_lines = find_lines()

    add_name(input_lines['NameLine'], fullname)

    # TODO: allow odd number of skills
    last_skill = skill_list[-1]
    for skill in skill_list:
        if skill == last_skill:
            add_skill(input_lines['SkillLine'], skill[0], skill[1], end=True)
        else:
            add_skill(input_lines['SkillLine'], skill[0], skill[1])
    for work in work_list:
        add_work_exp(input_lines['WorkLine'], work[0], work[1], work[2], work[3], work[4])
    for edu in edu_list:
        add_edu(input_lines['EduLine'], edu[0], edu[1], edu[2], edu[3])

    # writes all changes to file
    with open(OUT_DIR + filename + '.tex', 'w+') as file_w:
        file_w.writelines(read_data)
    print("Created new {}.tex file".format(filename))

    print("Running pdflatex to compile {}.tex to pdf".format(filename))
    run_pdf(filename)


# edit_globals
#     changes where the injection lines would be found
def find_lines():
    result = {'NameLine': -1, 'SkillLine': -1, 'WorkLine': -1, 'EduLine': -1}

    # line search
    for i in range(0, len(read_data)):
        item = read_data[i].strip()
        if item == NAME_TEXT and result['NameLine'] == -1:
            result['NameLine'] = i + 1
            i = 0

        if item == SKILL_TEXT and result['SkillLine'] == -1:
            result['SkillLine'] = i + 1
            i = 0

        if item == WORK_TEXT and result['WorkLine'] == -1:
            result['WorkLine'] = i + 1
            i = 0

        if item == EDU_TEXT and result['EduLine'] == -1:
            result['EduLine'] = i + 1
            i = 0

    print(result)
    return result

# run_pdf
#     runs the command pdflatex with the given tex file
#     filename: name of the tex file, does not need the .tex extension
def run_pdf(filename):
    full_file = OUT_DIR + filename + '.tex'
    os.system('pdflatex --output-directory={} {} '.format(OUT_DIR, full_file))

create_file("res1", "Some Dude", [["Python", "Java"], ["Something", "Nothing"]], 
[["Some Place", "Past", "Present", "Employee", ["Swept floors", "Cleaned dishes", "Cleaned restrooms", "Dumped Trash"]]], 
[["No Name Community College", "Sep. 2011", "Jun. 2013", "Associates Degree in Information and Technology"]])

# main()
