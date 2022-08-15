import os
import sys
import winreg

__SUBKEY_PATH = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon'
__VALUE_NAME = 'Shell'


def _generate_launch_command(config_path: str) -> str:
    return '"' + sys.argv[0] + '" -c "' + config_path + '"'


def install(config_path: str):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, __SUBKEY_PATH, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, __VALUE_NAME, 0, winreg.REG_SZ, _generate_launch_command(config_path))


def uninstall():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, __SUBKEY_PATH, 0, winreg.KEY_SET_VALUE)
    winreg.DeleteValue(key, __VALUE_NAME)


def check_installed() -> bool:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, __SUBKEY_PATH)
    try:
        val = winreg.QueryValueEx(key, __VALUE_NAME)[0]
    except FileNotFoundError:
        return False
    return val.startswith('"' + sys.argv[0] + '"')
