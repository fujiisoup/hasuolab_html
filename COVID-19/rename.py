import os
from shutil import copyfile

files = ['matome.html']
replace_list_file = 'rename_list.csv'

replace_list = []
with open(replace_list_file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        old_name, new_name = [item.strip() for item in line.split(',')]
        replace_list.append((old_name.replace("'", ""), new_name))

# copy the file
for replace in replace_list:
    try:
        copyfile(replace[0], replace[1])
    except FileNotFoundError:
        pass

# update html
for file in files:
    with open(file, 'r') as f:
        lines = f.readlines()
    
    for replace in replace_list:
        lines = [
            line.replace('href="./' + replace[0], 'href="./' + replace[1])
            for line in lines
        ]
    with open(file, 'w') as f:
        for line in lines:
            f.write(line)
    
