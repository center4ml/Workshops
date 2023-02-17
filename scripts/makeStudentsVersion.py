#!/bin/python3

import os
import subprocess
import glob
from termcolor import colored

testRun = False

result = subprocess.run(["git", "branch","--show-current"], text=True, capture_output=True)
branch_name = result.stdout
branch_name = branch_name.rstrip("\n")

print(colored("Commiting curent changes to solution branch.","blue"))
if not testRun:
    subprocess.run(["git", "commit","-a", "-m automatic commit"])

print(colored("Switching to students branch.","blue"))
students_branch_name = branch_name.replace("_solutions","")
if not testRun:
    result = subprocess.run(["git", "checkout",students_branch_name], text=True, capture_output=True)
print(colored("Removing solutions blocks.","blue"))

result = subprocess.run(["git","diff","--name-only", branch_name, students_branch_name], text=True, capture_output=True)
fileList = result.stdout.rstrip("\n").split("\n")

for aFile_name in fileList:
    if aFile_name.find("README")!=-1 or  aFile_name.find("makeStudentsVersion.py")!=-1:
        continue
    input_file_name = aFile_name
    output_file = open("tmp.ipynb", "w")
    subprocess.run(["git","restore", "--source",branch_name,"--",aFile_name], text=True, capture_output=True)
    result = subprocess.run(["git","add",aFile_name], text=True, capture_output=True)
    result = subprocess.run(["awk", " /#BEGIN_SOLUTION/{p=1}/#END_SOLUTION/{p=0;print \"    \\\"...\\\\n\\\", \";next}!p", input_file_name],
                            text=True, stdout=output_file)
    if not testRun:
        subprocess.run(["mv","tmp.ipynb",input_file_name])
    
print(colored("Commiting curent changes to students branch.","blue"))
if not testRun:
    subprocess.run(["git", "status"])
    subprocess.run(["git", "commit","-a", "-m automatic commit"])

print(colored("Switching back to solutions branch.","blue"))
if not testRun:
    subprocess.run(["git", "checkout",branch_name], text=True, capture_output=True)
