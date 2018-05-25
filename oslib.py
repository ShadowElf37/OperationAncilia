import platform
import socket
import subprocess
import shlex

class Interface:
    PTYPE = {'Windows': 'W', 'Darwin': 'M', 'Linux': 'L'}

    def __init__(self):
        self.os_name = platform.system() + ' ' + platform.release()
        self.os_type = Interface.PTYPE.get(platform.system(), 'O')
        self.encoding = 'UTF-8'

    def get_os(self, verbose=False):
        return self.os_type if not verbose else self.os_name

    def get_network_name(self):
        return socket.getfqdn()

    def get_IPv4(self):
        return socket.gethostbyname(socket.getfqdn())

    def get_battery_info(self):
        if self.os_type == 'M':
            return self.cmd('pmset -g batt')

    def cmd(self, cmd):
        return subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).stdout.decode(self.encoding)