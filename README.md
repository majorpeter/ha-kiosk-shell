# Home Automation Kiosk Shell

## What this is

This is a configurable Python application that can download a file from TFTP, search for patterns in it and launch other applications when a pattern is found. It can be installed as a replacement shell for a user on Windows.

## The use case

My PC is used for development on Linux and gaming on Windows. It is also part of my home automation setup and can be started with either OS remotely. Note that it's also far away from the TV.

This tool allows me to boot into a game library ([Playnite](https://playnite.link/)) with controller support without a keyboard and a mouse (with autologon). It can also log out of the autologon session if Windows not started for gaming only.

## Installation

* (Optional) Create a virtualenv and install into it
* Install package: `pip install .`
* (Optional) Create a new user that will be used for this kind of kiosk mode
* Run `ha-kiosk-shell -h` under _venv/Scripts_ for help, and proceed with the installation steps below
* Enable auto login on Windows to the preferred user and set `logout` as the `fallback` action in the config

## Usage/Configuration

The `ha-kiosk-shell` entry point can be used for configuration and debugging. The `-h` argument shows the help text. Create a configuration _YAML_ file (copy the template), and edit it. It can used with the `-c`/`--config` argument. 

### Commands

* `execute` (default): Run the configuration (download command file and execute accordingly)
* `install`: install as default shell for current user
* `uninstall`: remove shell setting from registry (reverts to Windows default)
* `check-installed`: check whether it's installed or not

### No console

Once the configuration is ready, you no longer need the console window to appear. So use the other entry point to install again:

```
ha-kiosk-shell-hidden -c <my-config-file-path> install
```

## Troubleshooting

If the executable/config is moved or deleted, the shell won't open. Ctrl+Alt+Del allows you to run Task Manager and you can launch the original shell from it: _File_ menu > _New Task_, and run `explorer`. You can fix or uninstall from there.

## Possible future improvements

* multiple commands in parallel or sequence
* Linux support
* option to restart with new command (without relogin/PC restart)
* support for Windows auto login setup with administrator privileges
