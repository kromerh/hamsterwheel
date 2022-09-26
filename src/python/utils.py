"""
================================================================================
Author:      Heiko Kromer - 2022
Description: This script contains utility functions used in hamsterwheel.py
================================================================================
"""
from typing import Tuple, Optional
from datetime import datetime
import logging
import sys
import os

import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def log(log_path: str, logmsg: str, printout: bool = False) -> None:
    """Function to add a line to a logfile.

    Args:
        log_path: Full path to the filename with the log.
        logmsg: Message to be appended to the log file.
        printout: If True, `logmsg` is also printed out. Defaults to False.

    Returns:
        None.
    """
    # Add the current timestamp to the log
    logmsg = f'{datetime.now()} - {logmsg}'

    if printout:
        logger.info(f"## Added log message: {logmsg}.")

    with open(log_path, 'a') as file:
        file.write('\n')
        file.write(logmsg)
        file.close()




s3 = boto3.resource('s3')

def download_s3_folder(bucket_name: str, s3_folder: str, local_dir: str =None):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_folder):
        target = obj.key if local_dir is None \
            else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == '/':
            continue
        bucket.download_file(obj.key, target)
