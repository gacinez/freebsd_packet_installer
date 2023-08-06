import re

import paramiko
import logging
from contextlib import contextmanager

from paramiko.ssh_exception import AuthenticationException, SSHException


class SSHClient:
    def __init__(self, host: str, username: str, password: str, port: int = 22):
        """Initialise SSHClient client object"""
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # logging.log(level='INFO')

    @contextmanager
    def _ssh_manager(self):
        """Context manager for paramiko ssh client"""
        try:
            self.client.connect(self.host, self.port, self.username, self.password)
            yield self.client
        except AuthenticationException:
            logging.error(
                f"Authentication failed, please verify your credentials: username - {self.username}, password - {self.password}")
        except SSHException as sshException:
            logging.error("Unable to establish SSH connection: %s" % sshException)
        finally:
            self.client.close()

    def execute_command(self, command: str) -> str:
        """Run command on remote server"""
        with self._ssh_manager() as client:
            stdin, stdout, stderr = client.exec_command(command, get_pty=True)
            out = stdout.read().decode('UTF-8').strip()
            for line in stdout.readlines():
                logging.warning(line)
            error = stderr.read().decode('UTF-8').strip()
            if error:
                logging.error('There was an error pulling the runtime: {}'.format(error))
            return out

    @staticmethod
    def _parse_file_name(filepath):
        pattern = r'[^//]*$'
        return re.search(pattern, filepath).group()

    def transfer_file(self, file_path: str):
        with self._ssh_manager() as client:
            sftp = client.open_sftp()
            out = sftp.put(file_path, f'/var/tmp/{self._parse_file_name(file_path)}')
            return out
