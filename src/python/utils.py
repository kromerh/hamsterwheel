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

    with open(log_path, 'a') as f:
        f.write('\n')
        f.write(logmsg)
        f.close()
