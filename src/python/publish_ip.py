import os
from datetime import datetime
import subprocess
import time
from typing import List
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from utils import log

from constants import (
    BASH_GET_WLAN,
    LOG_PUBLISHIP,
    AWS_CLIENT_NAME,
    AWS_ENDPOINT,
    AWS_CA_FILE,
    AWS_KEY,
    AWS_CERT,
)


class PublishIp():
    """Class to send the IP address of the RaspberryPi and the user name to
    AWS IoT.

    Attributes:
        username: username on the RaspberryPi. The output from the scripts to retrieve
            the `ifconfig`-content will be stored in the home folder of this user.
        path_to_bash: Full path to the script to retrieve ifconfig information.
    """

    def __init__(
        self,
        username: str = None,
        path_to_bash: str = None
    ) -> None:
        self.username = PublishIp._get_username() if username == None else username
        if path_to_bash:
            self.path_to_bash = path_to_bash
        else:
            self.path_to_bash = PublishIp._path_get_wlan_info(username=self.username)

    @classmethod
    def _get_username(cls) -> str:
        """Class method to retrieve the RaspberryPi user name.

        Returns:
            Linux user name.
        """
        username = os.getlogin()
        msg = f'Linux user name is {username}'
        log(log_path=LOG_PUBLISHIP, logmsg=msg, printout=True)

        return username

    @classmethod
    def _path_get_wlan_info(cls, username: str) -> str:
        """Class method to retrieve the path to the bash script which executes
        the code to read the output of the `ifconfig`-command

        Args:
            username: Linux username.

        Returns:
            Path to the bash script to retrieve `ifconfig`.
        """
        path_to_bash = f'/home/{username}/{BASH_GET_WLAN}'
        msg = f'Path to bash is {path_to_bash}'
        log(log_path=LOG_PUBLISHIP, logmsg=msg, printout=True)
        return path_to_bash

    def setup_aws(self) -> None:
        """Method to set up communication with AWS.

        """
        mqtt_client = AWSIoTMQTTClient(AWS_CLIENT_NAME)
        mqtt_client.configureEndpoint(AWS_ENDPOINT, 8883)

        mqtt_client.configureCredentials(
            CAFilePath=AWS_CA_FILE,
            KeyPath=AWS_KEY,
            CertificatePath=AWS_CERT
        )
        return mqtt_client

    def read_ifconfig(self) -> List[str]:
        """Method to retrieve the content of the ifconfig file. Will be stored in the users home
        directory.

        Returns:
            Content of ifconfig.
        
        Raises:
            ValueError if retrieval was not successful.
        """
        assert self.username is not None

        # Load the wlan information from file
        ifconfig_file = f'/home/{self.username}/ifconfig.txt'
        file_content: List[str] = []
        with open(ifconfig_file, 'r') as file:
            file_content = file.readlines()
            file.close()

        msg = f'Read {len(file_content)} lines in ~/ifconfig.txt'
        log(log_path=LOG_PUBLISHIP, logmsg=msg, printout=True)
        
        return file_content

    def run_bash(self) -> None:
        """Method to run the bash script to retrieve the ifconfig content.

        Will be stored in the home directory in a file named "ifconfig.txt:.
        """
        assert self.path_to_bash is not None
        subprocess.call(['sh', self.path_to_bash])
        msg = 'Started bash to read ifconfig.'
        log(log_path=LOG_PUBLISHIP, logmsg=msg, printout=True)
    
    def clean_ifconfig_file(self, file_content: List[str]) -> List[str]:
        """Method to clean the ifconfig file content.

        Args:
            file_content: Content of the ifconfig file.

        Returns:
            Cleaned ifconfig file.
        """

        # Clean the file info to extract only wlan0 content
        nr_extract: int = 0
        for i, line in enumerate(file_content):
            if 'wlan0' in line:
                nr_extract = i

        file_content = [f.strip() for f in file_content[nr_extract:]]

        return file_content

    def publish_message(self, mqtt_client, file_content: List[str]) -> None:
        """Method to publish message to AWS with the ifconfig wlan information.
        """
        assert self.username is not None
        topic = f'topic/{self.username}'

        now = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
        message = ''.join(file_content)
        topic = f'topic/{self.username}'
        mqtt_connection = mqtt_client.connect()
        mqtt_client.publish(
            topic,
            "{\"Timestamp\" :\"" + str(now) +
            "\", \"ifconfig\":\"" + message + "\"}", 0)
        msg = 'Published to topic {topic} with message {message}.'
        log(log_path=LOG_PUBLISHIP, logmsg=msg, printout=True)


if __name__ == "__main__":
    publish_ip = PublishIp()
    # Run the bash to retrieve ifconfig and save to ifconfig.txt
    publish_ip.run_bash()
    # Read ifconfig content
    ifconfig_content = publish_ip.read_ifconfig()
    # Clean ifconfig content
    ifconfig_content = publish_ip.clean_ifconfig_file(file_content=ifconfig_content)
    # Connect to AWS
    mqtt_client = publish_ip.setup_aws()
    print(type(mqtt_client))
    # Publish mesage
    publish_ip.publish_message(mqtt_client=mqtt_client, file_content=ifconfig_content)