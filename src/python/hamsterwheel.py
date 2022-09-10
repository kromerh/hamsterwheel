import sys
import time
from typing import List, Optional

import RPi.GPIO as io

from constants import FILENAME_LOG_HAMSTERWHEEL
from utils import log


class HamsterWheel():
    """Class to handle data collection for the hamsterwheel.

    Attributes:
        mode: Controls output location of the sensor data.
            Currently supports: local, aws
        wheelpin: GPIO pin to communicate with the reed sensor.
        local_log_path: Full path to store the readout data in local mode.
            Is required if 'local' is part of `mode`.
    """
    supported_modes = ['local', 'aws']

    def __init__(
        self,
        mode: List[str],
        wheelpin: int,
        local_log_path: Optional[str] = None,
    ) -> None:
        self._local_log_path = local_log_path
        self._mode = HamsterWheel._validate_mode(mode=mode, local_log_path=local_log_path)
        self._wheelpin = HamsterWheel._validate_wheelpin(wheelpin=wheelpin)

    @classmethod
    def _validate_mode(cls, mode: List[str], local_log_path: Optional[str] = None) -> List[str]:
        """Class method to validate user input.

        Args:
            mode: Mode input argument.
            local_log_path: Full path to store the readout data in local mode.

        Returns:
            Mode if it is a part of the supported modes.

        Raises:
            ValueError if the user input is not supported.
        """
        try:
            assert isinstance(mode, list)
            for set_mode in mode:
                assert set_mode in HamsterWheel.supported_modes
        except AssertionError:
            errmsg = f'Mode {mode} is not among the supported modes {HamsterWheel.supported_modes}.'
            raise ValueError(errmsg) from AssertionError

        # Make sure that a file path for local storage is set
        if 'local' in mode:
            try:
                assert isinstance(local_log_path, str)
            except AssertionError:
                errmsg = f'local mode requires `local_log_path` which is {local_log_path} and this is not valid.'
                raise ValueError(errmsg) from AssertionError

        return mode

    @classmethod
    def _validate_wheelpin(cls, wheelpin: int) -> int:
        """Class method to validate user input.

        Args:
            wheelpin: Wheelpin input argument.

        Returns:
            Wheelpin if it is a valid integer.

        Raises:
            ValueError if the user input is not supported.
        """
        try:
            assert isinstance(wheelpin, int)
            assert wheelpin > 0
            assert wheelpin < 40

        except AssertionError:
            errmsg = f'Wheelpin {wheelpin} is supported. Must be smaller 40 and larger 0.'
            raise ValueError(errmsg) from AssertionError

        return wheelpin

    def _setup_rpi(self) -> None:
        """Method to set up the GPIO on the RaspberryPi.
        """
        # Set Broadcom mode so we can address GPIO pins by number.
        io.setmode(io.BCM)

        io.setup(self._wheelpin, io.IN, pull_up_down=io.PUD_UP)
        msg = f'Set up GPIO, using wheel pin {self._wheelpin}'
        log(log_path=self._local_log_path, logmsg=msg, printout=True)

    def _setup_aws(self) -> None:
        """Method to set up communication with AWS.
        """
        return None

    def readout(self) -> None:
        """Method to start the readout of the reed sensor.

        If readout mode 'local', puts pin_state in the logfile.
        If readout mode 'aws', sends message to specified endpoint.
        """
        msg = 'Started script...'
        log(log_path=self._local_log_path, logmsg=msg, printout=True)

        try:
            # Readout loop
            while True:
                msg = 'Running...'
                log(log_path=self._local_log_path, logmsg=msg, printout=True)
                time.sleep(0.01)
                if io.input(self._wheelpin) == 0:
                    if 'local' in self._mode:
                        msg = 'pin_state = 0'
                        log(log_path=self._local_log_path, logmsg=msg, printout=True)
                    if 'aws' in self._mode:
                        pass
                else:
                    if 'local' in self._mode:
                        msg = 'pin_state = 1'
                        log(log_path=self._local_log_path, logmsg=msg, printout=True)
                    if 'aws' in self._mode:
                        pass

        except KeyboardInterrupt:
            sys.exit()


if __name__ == "__main__":
    hamsterwheel = HamsterWheel(mode=['local'], wheelpin=18, local_log_path=123)
    hamsterwheel.readout()
