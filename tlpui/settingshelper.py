"""This module provides helper functions for application settings."""

import configparser
import re
import sys
from os import getenv
from subprocess import check_output
from pathlib import Path


def get_tlp_config_file(version: str, prefix: str) -> str:
    """Select tlp config file path by version."""
    if version in ["0_8", "0_9", "1_0", "1_1", "1_2"]:
        return f"{prefix}/etc/default/tlp"
    return f"{prefix}/etc/tlp.conf"


def get_installed_tlp_version() -> str:
    """Fetch tlp version from command."""
    pattern = re.compile(r"TLP ([^\s]+)")
    currentconfig = check_output(["tlp-stat", "-c"]).decode(sys.stdout.encoding)
    matcher = pattern.search(currentconfig)
    version = matcher.group(1).replace(".", "_")
    return version


def get_installed_major_minor_version() -> str:
    """Fetch tlp major and minor version."""
    return get_installed_tlp_version()[0:3]


def get_user_config_file() -> Path:
    """Get config path for executing user."""
    userconfighome = getenv("XDG_CONFIG_HOME", "")
    if userconfighome == "":
        userconfigpath = Path(str(Path.home()) + "/.config/tlpui")
    else:
        userconfigpath = Path(str(userconfighome) + "/tlpui")
    return Path(str(userconfigpath) + "/tlpui.cfg")


class UserConfig:
    """Class to handle ui config parameters."""

    def __init__(self):
        """Init user config class parameters."""
        self.language = "en_EN"
        self.activeoption = 0
        self.activecategory = 0
        self.windowxsize = 900
        self.windowysize = 600
        self.userconfigfile = get_user_config_file()
        self.read_user_config()

    def read_user_config(self):
        """Read ui config parameters from user home."""
        if self.userconfigfile.exists():
            config = configparser.ConfigParser()
            with open(str(self.userconfigfile)) as configfile:
                config.read_file(configfile)
            try:
                self.language = config['default']['language']
                self.activeoption = int(config['default']['activeoption'])
                self.activecategory = int(config['default']['activecategory'])
                self.windowxsize = int(config['default']['windowxsize'])
                self.windowysize = int(config['default']['windowysize'])
            except KeyError:
                # Config key error, override with default values
                self.write_user_config()
        else:
            self.userconfigfile.parent.mkdir(parents=True, exist_ok=True)
            self.write_user_config()

    def write_user_config(self):
        """Persist ui config parameters to user home."""
        config = configparser.ConfigParser()
        config['default'] = {}
        config['default']['language'] = self.language
        config['default']['activeoption'] = str(self.activeoption)
        config['default']['activecategory'] = str(self.activecategory)
        config['default']['windowxsize'] = str(self.windowxsize)
        config['default']['windowysize'] = str(self.windowysize)
        with open(str(self.userconfigfile), 'w') as configfile:
            config.write(configfile)
