import os
from datetime import datetime
import subprocess
import time
from typing import List
from subprocess import Popen, PIPE
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

    def setup_aws(self) -> AWSIoTMQTTClient:
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
        time.sleep(0.1)
    
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

    def publish_message(self, mqtt_client: AWSIoTMQTTClient, message: str) -> None:
        """Method to publish message to AWS with the ifconfig wlan information.
        """
        assert self.username is not None

        now = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
        
        topic = f'topic/publish_ip'
        mqtt_connection = mqtt_client.connect()
        mqtt_client.publish(
            topic,
            "{\"Timestamp\" :\"" + str(now) +
            "\", \"username\" :\"" + str(self.username) +
            "\", \"ip\":\"" + message + "\"}", 0)
        msg = f'Published to topic {topic} with message {message}.'
        log(log_path=LOG_PUBLISHIP, logmsg=msg, printout=True)

    def find_interface(self) -> str:
        """Method to find the device name looking for an active Ethernet or WiFi device

        Returns:
            Device name as string.
        """
        find_device = "ip addr show"
        interface_parse = self.run_cmd(cmd=find_device)
        for line in interface_parse.splitlines():
            if "state UP" in line:
                dev_name = line.split(':')[1]

        return dev_name

    def parse_ip(self, interface: str) -> str:
        """Method to find an active IP on the first live network device.

        Args:
            interface: Device name.
        
        Returns:
            IP address of the interface device
        """
        find_ip = f"ip addr show {interface}"
        find_ip = f"ip addr show {interface}"
        ip_parse = self.run_cmd(cmd=find_ip)
        for line in ip_parse.splitlines():
            if "inet " in line:
                ip = line.split(' ')[5]
                ip = ip.split('/')[0]

        return ip

    def run_cmd(self, cmd: str) -> str:
        """Method to run a command via Popen.

        Args:
            cmd: Command to run.
        
        Returns:
            Response from the command.
        """
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]

        return output.decode('ascii')


if __name__ == "__main__":
    # -------------------------------------------------------------------------------- #
    # Use below commented out commented oll the content in ifconfig
    # -------------------------------------------------------------------------------- #
    # publish_ip = PublishIp()
    # # Run the bash to retrieve ifconfig and save to ifconfig.txt
    # publish_ip.run_bash()
    # # Read ifconfig content
    # ifconfig_content = publish_ip.read_ifconfig()
    # # Clean ifconfig content
    # ifconfig_content = publish_ip.clean_ifconfig_file(file_content=ifconfig_content)
    # # Connect to AWS
    # mqtt_client = publish_ip.setup_aws()
    # # Publish mesage
    # message = ''.join(ifconfig_content)
    # publish_ip.publish_message(mqtt_client=mqtt_client, message=message)
    # -------------------------------------------------------------------------------- #
    # Use below to find only IP address
    # -------------------------------------------------------------------------------- #
    publish_ip = PublishIp()
    interface = publish_ip.find_interface()
    ip_address = publish_ip.parse_ip(interface=interface)
    # # Connect to AWS
    mqtt_client = publish_ip.setup_aws()
    # # Publish mesage
    publish_ip.publish_message(mqtt_client=mqtt_client, message=ip_address)
