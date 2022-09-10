"""
================================================================================
Author:      Heiko Kromer - 2022
Description: This script contains constants used in hamsterwheel.py
================================================================================
"""
# Flag to control if the script will be run locally on the Pi or from remote
_REMOTE = False

# RPi paths
HOME = '/home/wilson/'
REPO = 'repo'
BASH = '/src/bash/'
LOGS = '/logs/'

# Bash script to start the readout
FILENAME_RUN_HAMSTERWHEEL = 'run_hamsterwheel.sh'
# Log file for the hamsterwheel readout code
FILENAME_LOG_HAMSTERWHEEL = 'hamsterwheel.log'
# Log file for the handler of the script
FILENAME_LOG_HAMSTERWHEEL_HANDLER = 'hamsterwheel_handler.log'

SH_HAMSTERWHEEL = f'{HOME}{REPO}{BASH}{FILENAME_RUN_HAMSTERWHEEL}'
LOG_HAMSTERWHEEL = f'{HOME}{LOGS}{FILENAME_LOG_HAMSTERWHEEL}'

# Database
# Database connection strings
DATABASE = 'hamsterwheel_db'
if _REMOTE:
    HOST = 'xxx.xxx.xxx.xxx'  # Edit for remote access
else:
    HOST = 'localhost'  # On the RPi local
PORT = 3306
FULL_PATH_TO_CREDENTIALS = f'{HOME}/credentials.cred'
# For execution on another host

# Table for the wheel data
NO_END_TIME = '0000-00-00 00:00:00.000000'
TABLE_HAMSTERWHEEL = 'hamsterwheel'
