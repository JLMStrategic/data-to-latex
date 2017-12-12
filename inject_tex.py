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


# Which line in TeX file to append to
NAME_LINE = -1
SKILL_LINE = -1
WORK_LINE = -1
EDU_LINE = -1

# Open the TeX file and store onto read_data list
with open(CWD + '/JLM_Resume.tex', 'r') as f:
    read_data = f.readlines()


# add_name function
#     adds skill1 and skill2 onto the skills section of the TeX file
#     name: person's full name {first, middle, last} as a string
def add_name(name):
    add_name = '\\Huge{{{}}}'.format(name)
    read_data[NAME_LINE] = read_data[NAME_LINE].strip() + add_name

    print("Added name: {}".format(name))


# add_skill function
#     adds skill1 and skill2 onto the skills section of the TeX file
#     skill1: skill to appear on left side
#     skill2: skill to appear on right side
#     end: last skills bullets will not have extra padding. default=False
def add_skill(skill1, skill2, end=False):
    add_line = '\\skillItem{{{}}}{{{}}}\n'.format(skill1, skill2)
    add_line_end = '\\skillItemEnd{{{}}}{{{}}}\n'.format(skill1, skill2)

    # inject add_line one the SKILL_LINE on TeX doc
    if end:
        read_data[SKILL_LINE] = read_data[SKILL_LINE].strip() + add_line_end
    else:
        read_data[SKILL_LINE] = read_data[SKILL_LINE].strip() + add_line

    print("Added {} and {} as skill 1 and skill 2".format(skill1, skill2))


#  add_work_exp function
#     creates a new work experience section for the TeX file
#     company: name of the company
#     start_date: date started working
#     end_date: date ended working
#     position: job title
#     desc: list of descriptions for this specific job
def add_work_exp(company, start_date, end_date, position, desc):
    new_work = '\\newWorkExp{{{}}}{{{}}}{{{}}}{{{}}}'.format(
        company, start_date, end_date, position)
    work_sec_start = '\\workExpStart'
    work_sec_end = '\\workExpEnd'
    desc_items = ''

    for item in desc:
        desc_items += add_work_desc(item)

    # inject new_work block onto TeX file
    read_data[WORK_LINE] = read_data[WORK_LINE].strip() +\
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
def add_edu(school, start_date, end_date, degree):
    new_edu = '\\newEducation{{{}}}{{{}}}{{{}}}{{{}}}'.format(school, start_date, end_date, degree)
    read_data[EDU_LINE] = read_data[EDU_LINE].strip() + new_edu

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
    edit_globals()

    add_name(fullname)

    # TODO: allow odd number of skills
    last_skill = skill_list[-1]
    for skill in skill_list:
        if skill == last_skill:
            add_skill(skill[0], skill[1], end=True)
        else:
            add_skill(skill[0], skill[1])
    for work in work_list:
        add_work_exp(work[0], work[1], work[2], work[3], work[4])
    for edu in edu_list:
        add_edu(edu[0], edu[1], edu[2], edu[3])

    # writes all changes to file
    with open(OUT_DIR + filename + '.tex', 'w+') as file_w:
        file_w.writelines(read_data)
    print("Created new {}.tex file".format(filename))

    print("Running pdflatex to compile {}.tex to pdf".format(filename))
    run_pdf(filename)


# edit_globals
#     changes where the injection lines would be found
def edit_globals():
    global NAME_LINE
    global SKILL_LINE
    global WORK_LINE
    global EDU_LINE

    # line search
    for i in range(0, len(read_data)):
        item = read_data[i].strip()
        if item == NAME_TEXT and NAME_LINE == -1:
            NAME_LINE = i + 1
            i = 0

        if item == SKILL_TEXT and SKILL_LINE == -1:
            SKILL_LINE = i + 1
            i = 0

        if item == WORK_TEXT and WORK_LINE == -1:
            WORK_LINE = i + 1
            i = 0

        if item == EDU_TEXT and EDU_LINE == -1:
            EDU_LINE = i + 1
            i = 0


# run_pdf
#     runs the command pdflatex with the given tex file
#     filename: name of the tex file, does not need the .tex extension
def run_pdf(filename):
    full_file = OUT_DIR + filename + '.tex'
    os.system('pdflatex --output-directory={} {} '.format(OUT_DIR, full_file))


# main function for testing, running, etc.
def main():
    # testing
    edit_globals()

    add_name("Some Dudes")
    add_skill("Dish Wash", "Cashier")
    add_skill("Python", "Java")
    add_skill("Something", "Nothing", end=True)
    add_work_exp("Some Place", "Past", "Present", "Employee",
                 ["Swept floors", "Cleaned dishes", "Cleaned restrooms", "Dumped Trash"])
    add_work_exp("Another Place", "Past", "Present", "Boss", ["Slacked Off", "Drank Soda"])
    add_edu("University of Califonia, Davis", "Sep. 2013",
            "Jun. 2017", "Bachelor's of Science, Computer Science")
    add_edu("No Name Community College", "Sep. 2011",
            "Jun. 2013", "Associates Degree in Information and Technology")

create_file("res1", "Some Dude", [["Python", "Java"], ["Something", "Nothing"]], 
[["Some Place", "Past", "Present", "Employee", ["Swept floors", "Cleaned dishes", "Cleaned restrooms", "Dumped Trash"]]], 
[["No Name Community College", "Sep. 2011", "Jun. 2013", "Associates Degree in Information and Technology"]])

# main()
