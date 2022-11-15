#!/bin/python3

import os, sys
import subprocess
import glob

nInputParams = len(sys.argv)
input_file_name = ""
if nInputParams<2:
    print("No input file proivided! Usage:")
    print("makeStudentsVersion.py notebook.ipynb")
    exit(1)
else:
    input_file_name = sys.argv[1]
    
print("Modyfying file:", input_file_name)
output_file = open("tmp.ipynb", "w")
result = subprocess.run(["awk", " /#BEGIN_SOLUTION/{p=1}/#END_SOLUTION/{p=0;print \"    \\\"...\\\\n\\\", \";next}!p", input_file_name],
                        text=True, stdout=output_file)

subprocess.run(["mv","tmp.ipynb",input_file_name])
    
print("Done.")

