import os
from argparse import ArgumentParser
from enum import Enum
from io import BytesIO

import yaml
from tftpy import TftpClient

import installer


class WindowsShutdownCommands:
    @staticmethod
    def logout_user():
        os.system('shutdown -l')

    @staticmethod
    def shutdown():
        os.system('shutdown /s /t 1')

    @staticmethod
    def reboot():
        os.system('shutdown /s /t 1')


def fetch_command_file(config):
    file = BytesIO()
    TftpClient(config['tftp_host']).download(config['tftp_file'], file)
    file.seek(0)
    return file.read().decode('ascii')


keyword_actions = {
    'logout': WindowsShutdownCommands.logout_user,
    'shutdown': WindowsShutdownCommands.shutdown,
    'reboot': WindowsShutdownCommands.reboot,
}


def execute_configuration(config_file_path: str):
    with open(config_file_path, 'r') as f:
        config = yaml.full_load(f)
    command = fetch_command_file(config['command_file'])

    for c in config['commands']:
        if 'contains' in c and c['contains'] in command:
            os.system(c['exec'])
            if 'then' in c:
                keyword_actions[c['then']]()
            exit(0)

    if 'fallback' in config:
        if config['fallback'] in keyword_actions:
            keyword_actions[config['fallback']]()
        else:
            os.system(config['fallback'])


class CommandArgument(Enum):
    Execute = 'execute'
    Install = 'install'
    Uninstall = 'uninstall'
    CheckInstalled = 'check-installed'


if __name__ == '__main__':
    parser = ArgumentParser('Home Automation Kiosk Shell')
    parser.add_argument('-c', '--config', help='Set path for config.yaml')
    parser.add_argument('command', default=CommandArgument.Execute.value,
                        choices=[value.value for name, value in CommandArgument.__members__.items()], nargs='?')
    args = parser.parse_args()

    if args.config is None:
        # fall back to 'config.yaml' file in application's folder
        args.config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')

    if args.command == CommandArgument.Execute.value:
        execute_configuration(args.config)
    elif args.command == CommandArgument.Install.value:
        installer.install()
        print('Installed')
    elif args.command == CommandArgument.Uninstall.value:
        installer.uninstall()
        print('Uninstalled')
    elif args.command == CommandArgument.CheckInstalled.value:
        if installer.check_installed():
            print('Is installed')
        else:
            print('NOT installed')
