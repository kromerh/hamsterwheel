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

print(file_content)