from helper.PacketInstaller import PacketInstaller


if __name__ == "__main__":
    installer = PacketInstaller(packet_source_code='packages/cowsay-3.03.tar.gz')
    # command = installer.ex_com('cd /tmp && ls -la')
    command = installer.install_from_local()
