import logging

from SSHClientContextManager import SSHClientContextManager
from constants import *


class PacketInstaller:

    def __init__(self):
        self.ssh_manager = SSHClientContextManager(host=HOSTNAME, username=USERNAME, password=PASSWORD)

    def execute_ssh_command_and_fail_if_stderr(self, command):
        """

        :param command:
        :return:
        """
        with self.ssh_manager as client:
            logging.info("Executing command: {cmd}".format(cmd=command), "DEBUG")
            stdin, stdout, stderr = client.exec_command(command)
            err = " ".join(stderr.readlines())
            out = " ".join(stdout.readlines())
            if err:
                logging.error(msg=err)
            else:
                logging.info(out, "INFO")
            return out.strip()

    def put_file(self, source, destination):
        """

        :param source:
        :param destination:
        :return:
        """
        with self.ssh_manager as client:
            logging.info(f"Put file {source} to destination {destination}")
            sftp_client = client.open_sftp()
            attributes = sftp_client.put(source, destination)
            sftp_client.close()
