"""Filehandling helper."""

import re
from io import open
from json import load


def get_json_schema_object_from_file(objectname: str, filename: str) -> dict:
    """Read Json file."""
    jsonfile = open(filename)
    jsonobject = load(jsonfile)
    jsonfile.close()
    return jsonobject[objectname]


class TlpDefaults:
    """TLP defaults class."""

    def __init__(self, name: str, value: str, enabled: bool):
        """Init TLP defaults class parameters."""
        self.name = name
        self.value = value
        self.enabled = enabled

    def get_name(self) -> str:
        """Get defaults name."""
        return self.name

    def get_value(self) -> str:
        """Get defaults value."""
        return self.value

    def is_enabled(self) -> bool:
        """Get defaults enabled."""
        return self.enabled


def extract_default_tlp_configs(filename: str) -> dict:
    """Fetch TLP defaults from file."""
    propertypattern = re.compile(r'^#?[A-Z_\d]+=')
    fileopener = open(filename)
    lines = fileopener.readlines()
    fileopener.close()

    tlpconfig_defaults = dict()
    for line in lines:
        if propertypattern.match(line):
            cleanline = line.lstrip().rstrip()

            if cleanline.startswith('#'):
                enabled = False
                cleanline = cleanline.lstrip('#')
            else:
                enabled = True

            configproperty = cleanline.split('=', maxsplit=1)
            configname = configproperty[0]
            configvalue = configproperty[1]

            if configvalue.startswith('\"') and configvalue.endswith('\"'):
                configvalue = configvalue.lstrip('\"').rstrip('\"')

            tlpconfig_defaults[configname] = TlpDefaults(configname, configvalue, enabled)
    return tlpconfig_defaults
