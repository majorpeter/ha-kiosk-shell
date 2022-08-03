import os
from argparse import ArgumentParser
from io import BytesIO

import yaml
from tftpy import TftpClient


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


if __name__ == '__main__':
    parser = ArgumentParser('Home Automation Kiosk Shell')
    parser.add_argument('-c', '--config', help='Set path for config.yaml')
    args = parser.parse_args()

    if args.config is None:
        # fall back to 'config.yaml' file in application's folder
        args.config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')

    with open(args.config, 'r') as f:
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
