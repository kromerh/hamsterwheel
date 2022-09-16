import os
import subprocess
import time

# Get the user
username = os.getlogin()

# Script to get the wlan information
bash_get_wlan = f'/home/{username}/hamsterwheel/src/bash/get_wlan.sh'

# Get the wlan ip
subprocess.call(['sh', bash_get_wlan])

# Sleep for a few seconds to allow bash script to retrieve wlan information
time.sleep(3)

# Load the wlan information from file
ifconfig_file = f'/home/{username}/ifconfig.txt'
with open(ifconfig_file, 'r') as file:
    file_content = file.readlines()
    file.close()

# Clean the file info to extract only wlan0 content
nr_extract: int = 0
for i, line in enumerate(file_content):
    if 'wlan0' in line:
        nr_extract = i

file_content = [f.strip() for f in file_content[nr_extract:]]

