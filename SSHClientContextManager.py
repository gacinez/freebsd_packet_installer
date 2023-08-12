import paramiko
import logging

from paramiko.ssh_exception import AuthenticationException, SSHException


class SSHClientContextManager:

    def __init__(self, host, username, password=None, port=22, key_filename=None):
        """

        :param host:
        :param username:
        :param password:
        :param port:
        :param key_filename:
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.key_filename = key_filename
        logging.basicConfig(format='[%(levelname)s] %(message)s - %(asctime)s', datefmt='%d-%b-%y %H:%M:%S')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def __enter__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # logging SSH connection start
        self.logger.info(f"Connecting to {self.host}:{self.port} as {self.username}...")
        try:
            self.client.connect(
                self.host,
                self.port,
                self.username,
                password=self.password,
                key_filename=self.key_filename
            )
            return self.client
        except AuthenticationException:
            logging.error("Authentication failed, please verify your credentials.")
        except SSHException as sshException:
            logging.error("Unable to establish SSH connection: %s" % sshException)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

        # logging SSH connection end
        self.logger.info(f"Disconnected from {self.host}:{self.port}")
