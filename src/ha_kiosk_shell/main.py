import logging
import os
from argparse import ArgumentParser
from enum import Enum
from io import BytesIO

import yaml
from tftpy import TftpClient

from ha_kiosk_shell import installer


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
    logging.info('Downloading file: tftp://{host}/{file}'.format(host=config['tftp_host'], file=config['tftp_file']))
    file = BytesIO()
    TftpClient(config['tftp_host']).download(config['tftp_file'], file)
    file.seek(0)
    file_data = file.read().decode('ascii')
    logging.debug('Received file contents:\n' + file_data)
    return file_data


keyword_actions = {
    'logout': WindowsShutdownCommands.logout_user,
    'shutdown': WindowsShutdownCommands.shutdown,
    'reboot': WindowsShutdownCommands.reboot,
}


def execute_configuration(config_file_path: str):
    logging.info('Loading config from {path}'.format(path=config_file_path))
    with open(config_file_path, 'r') as f:
        config = yaml.full_load(f)
    command = fetch_command_file(config['command_file'])

    for c in config['commands']:
        if 'contains' in c and c['contains'] in command:
            logging.info('Found \'{0}\' in command file'.format(c['contains']))

            logging.info('Executing \'{0}\'...'.format(c['exec']))
            os.system(c['exec'])
            logging.info('Execution of \'{0}\' finished'.format(c['exec']))

            if 'then' in c:
                keyword_actions[c['then']]()
            else:
                logging.info('All done')
            exit(0)

    logging.info('No match found in commands')
    if 'fallback' in config:
        logging.info('Executing fallback: ' + config['fallback'])
        if config['fallback'] in keyword_actions:
            keyword_actions[config['fallback']]()
        else:
            os.system(config['fallback'])


class CommandArgument(Enum):
    Execute = 'execute'
    Install = 'install'
    Uninstall = 'uninstall'
    CheckInstalled = 'check-installed'


def main():
    parser = ArgumentParser('Home Automation Kiosk Shell')
    parser.add_argument('-c', '--config', help='Set path for config.yaml')
    parser.add_argument('-v', '--verbose', action='store_true', help='More logs for debugging')
    parser.add_argument('command', default=CommandArgument.Execute.value,
                        choices=[value.value for name, value in CommandArgument.__members__.items()], nargs='?')
    args = parser.parse_args()

    logger = logging.getLogger('root')
    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
    if not args.verbose:
        logger.setLevel(logging.INFO)
        logging.getLogger('tftpy').setLevel(logging.WARNING)  # tftpy is quite verbose by default

    if args.config is None:
        # fall back to 'config.yaml' file in application's folder
        args.config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')

    if not os.path.exists(args.config):
        logger.error('Config file does not exist: ' + args.config)
        return

    if args.command == CommandArgument.Execute.value:
        execute_configuration(args.config)
    elif args.command == CommandArgument.Install.value:
        installer.install(config_path=os.path.abspath(args.config))
        print('Installed')
    elif args.command == CommandArgument.Uninstall.value:
        installer.uninstall()
        print('Uninstalled')
    elif args.command == CommandArgument.CheckInstalled.value:
        if installer.check_installed():
            print('Is installed')
        else:
            print('NOT installed')


if __name__ == '__main__':
    main()
