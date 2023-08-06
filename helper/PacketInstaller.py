from helper.SSHCLient import SSHClient
from helper import constants


class PacketInstaller:

    def __init__(self, packet_name: str = None, packet_source_code: str = None):
        self.packet_name = packet_name
        self.packet_source_code = packet_source_code
        self.ssh_client = SSHClient(host=constants.HOSTNAME,
                                    port=constants.PORT,
                                    username=constants.USERNAME,
                                    password=constants.PASSWORD)

    def install_from_pkg(self):
        return self.ssh_client.execute_command(f'pkg install -y {self.packet_name}')

    def ex_com(self, command):
        return self.ssh_client.execute_command(command)

    def run_packet(self, *args):
        command_string = f'{self.packet_name }'
        for arg in args:
            command_string += ' ' + arg
        return self.ssh_client.execute_command(command_string)

    def install_from_local(self):
        return self.ssh_client.transfer_file(self.packet_source_code)

    def install_from_git(self):
        pass
