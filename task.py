import re
from PacketInstaller import PacketInstaller

installer = PacketInstaller()


def parse_file_name(filepath):
    pattern = r'[^//]*$'
    return re.search(pattern, filepath).group()


def upload_file_and_make_install(file_path):
    file_name = parse_file_name(file_path)
    command_name = file_name.split('.')[0]
    destination = f'/var/tmp/{file_name}'
    installer.put_file(file_path, destination)
    installer.execute_ssh_command_and_fail_if_stderr(f'cd /var/tmp/')
    installer.execute_ssh_command_and_fail_if_stderr(f"tar -vxf {file_name} && cd {command_name} && make install && "
                                                     f"make clean")
    installer.execute_ssh_command_and_fail_if_stderr(command_name)

if __name__ == "__main__":
    upload_file_and_make_install('packages/cowsay-3.03.tar.gz')
