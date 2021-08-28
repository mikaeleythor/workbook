from datetime import date

def get_date():
    """Return date formatted for notebook"""
    return date.today().strftime("%B %d")

def get_week():
    return date.today().isocalendar()[1]-32 #MATCHING START OF FALL SEMESTER

def get_input():
    """Gets user input"""
    return input('Enter alnum paragraph: ')

def format_new_note(input_string):
    """Takes in user input and formats it to notebook entry"""
    return r"\subsection*{"+get_date()+"}" + '\n' + input_string + '\n'

def sectionstr_to_date(sectionstr):
    str_items = sectionstr.split()
    date = str_items[1].strip('}')
    mon = str_items[0].split('{')[1]
    return f'{mon} {date}'

def get_last_entry_date():
    tex_lines = read_tex_lines()
    for line in tex_lines[::-1]:
        if r"""\subsection*""" in line:
            return sectionstr_to_date(line)

def get_last_entry_week():
    tex_lines = read_tex_lines()
    for line in tex_lines[::-1]:
        if r"""\section*""" in line:
            return sectionstr_to_weeknum(line)

def sectionstr_to_weeknum(sectionstr):
    str_items = sectionstr.split()
    weeknum = str_items[1].strip('}')
    return int(weeknum)

def is_first_entry_today():
    return get_last_entry_date() != get_date()

def is_first_entry_of_week():
    return get_last_entry_week() != get_week()

def read_tex_lines():
    with open(workbook, 'r') as f:
        tex_lines = f.readlines()
    return tex_lines
    
### MAIN PROGRAM ### --------------------------------------------------------------------

PACKAGES = r"""\usepackage{caption}
\usepackage{graphicx}
\usepackage[margin=1.5cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[icelandic]{babel}
"""

CLASS = r"""\documentclass{article}
"""

TITLE = r"""\title{Workbook\\Mechatronics I}
\author{Eyþór Mikael Eyþórsson}
\begin{document}
\maketitle
"""

workbook = '/home/mcfuck/mechatronics/workbook/workbook.tex'

HEADER = CLASS+PACKAGES+TITLE

note = get_input()
if is_first_entry_today():
    entry = format_new_note(note)
else:
    entry = note+'\n'
if is_first_entry_of_week():
    entry = r'\section*{' + f'Week {get_week()}' + '}\n' + entry




with open(workbook, 'r') as d:
    tex_lines = d.readlines()
    # print(tex_lines)
    tex_lines.pop(-1)
    tex_lines.append(entry)
    tex_lines.append(r'\end{document}')

export_str = ''.join(tex_lines)

with open(workbook, 'w+') as c:
    c.write(export_str)


