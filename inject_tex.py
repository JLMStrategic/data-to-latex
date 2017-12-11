import os
import io

CWD = os.getcwd()

# Search for this exact string on TeX file to know
# which line to append to
SKILL_TEXT = '% SKILLS CODE HERE'
EXP_TEXT = '% EXP CODE HERE'
EDU_TEXT= '% EDU CODE HERE'

# Which line in TeX file to append to
SKILL_LINE = -1
EXP_LINE = -1
EDU_LINE = -1

# Open the TeX file and store onto read_data list
with open(CWD + '/JLM_Resume.tex', 'r') as f:
    # read_data = [line.strip() for line in f]
    read_data = f.readlines()

# add_skill function
#   adds skill1 and skill2 onto the skills section of the TeX file
#   skill1: skill to appear on left side
#   skill2: skill to appear on right side
def add_skill(skill1, skill2):
    add_line = '\\skillItem{{{}}}{{{}}}\n'.format(skill1, skill2)
    read_data[SKILL_LINE] = read_data[SKILL_LINE].strip() + add_line
    with open(CWD + '/JLM_Resume.tex', 'w') as f_w:
        f_w.writelines(read_data)
    print("Added {} and {} as skill 1 and skill 2".format(skill1, skill2))

# line search
for i in range(0, len(read_data)):
    item = read_data[i].strip()
    if item == SKILL_TEXT and SKILL_LINE == -1:
        SKILL_LINE = i + 1
        i = 0

    if item == EXP_TEXT and EXP_LINE == -1:
        i = 0
        EXP_TEXT = i + 1

    if item == EDU_TEXT and EDU_LINE == -1:
        i = 0
        EDU_LINE = i + 1

add_skill("Hello", "hi there")
