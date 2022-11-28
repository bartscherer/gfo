from typing import Any, Union
from yaml import load, SafeLoader

from gfo.config.static import Constants
from gfo.config.structure import CONFIGURATION_STRUCTURE
from gfo.exceptions import excstr
from gfo.exceptions.configuration import GConfigurationException

__GLOBAL_CONFIGURATION = None

class _ConfigurationReader(object):

    def __init__(self, config_file_path: str = Constants.Environment.CONFIG_FILE_PATH):
        self.config_file_path = config_file_path

    def get_config(self) -> dict:
        config = self.read_as_yaml_from_file()
        config = self.validate_and_complete_configuration(user_config_dict=config)
        return config

    def read_as_yaml_from_file(self) -> dict:
        try:
            with open(self.config_file_path, 'rb') as conf_stream: 
                configuration = load(
                    stream=conf_stream,
                    Loader=SafeLoader
                )
            if  configuration is None:
                configuration = {}
        except Exception as exc:
            raise GConfigurationException(
                f'Failed to read configuration from file "{self.config_file_path}". {excstr(exc)}'
            )
        return configuration

    def validate_and_complete_configuration(self, user_config_dict: dict) -> dict:
        parsed_configuration = {k: {} for k in CONFIGURATION_STRUCTURE}
        for key in user_config_dict:
            if not key in CONFIGURATION_STRUCTURE:
                raise GConfigurationException(
                    f'The configuration key "{key}" is not a recognized '
                    f'configuration setting. Valid keys: '
                    f'{",".join(CONFIGURATION_STRUCTURE.keys())}'
                )
            key_config_substructure = CONFIGURATION_STRUCTURE[key]
            custom_subconfig = user_config_dict[key]
            for subkey in custom_subconfig:
                if not subkey in key_config_substructure:
                    raise GConfigurationException(
                        f'The configuration key "{subkey}" is not a valid '
                        f'key for the configuration "{key}". Valid keys: '
                        f'{",".join(key_config_substructure.keys())}'
                    )
                subkey_custom_value = custom_subconfig[subkey]
                subkey_default = key_config_substructure[subkey]['default']
                subkey_description = key_config_substructure[subkey]['description']
                subkey_validator = key_config_substructure[subkey]['sanitizer']
                if subkey_default is not None and subkey_custom_value is None:
                    raise GConfigurationException(
                        f'The configuration setting "{key}.{subkey}" ({subkey_description}) '
                        f'is invalid. The value can not be None/null due to the default '
                        f'value of this setting not being None/null.'
                    )
                if subkey_default is None and subkey_custom_value is None:
                    parsed_configuration[key][subkey] = None
                    continue
                value, valid, errmsg = subkey_validator(subkey_custom_value)
                if not valid:
                    raise GConfigurationException(
                        f'The configuration setting "{key}.{subkey}" ({subkey_description}) '
                        f'is invalid. [{errmsg}]'
                    )
                parsed_configuration[key][subkey] = value
        for key in CONFIGURATION_STRUCTURE:
            for subkey in CONFIGURATION_STRUCTURE[key]:
                if not subkey in parsed_configuration[key]:
                    parsed_configuration[key][subkey] = CONFIGURATION_STRUCTURE[key][subkey]['default']
        return parsed_configuration

def from_config(key: str, subkey: Union[str, None] = None) -> Any:

    '''
        This method takes configuration key and optionally a subkey
        as parameters and returns the corresponding values from the
        global configuration read from the configuration YAML file
        and the defaults defined in ./structure.py.

        :param key: The key specifying the config topic
        :param subkey: The subkey within the config topic for :param key 
        :returns: All values for key (dict) if no subkey is provided else the value (Any) of the subkey within the config dict for "key"
        :raises GConfigurationException: when an unknown key/subkey was submitted or the configuration reader failed
    '''

    global __GLOBAL_CONFIGURATION
    if __GLOBAL_CONFIGURATION is None:
        config_reader = _ConfigurationReader()
        __GLOBAL_CONFIGURATION = config_reader.get_config()
    key = key.lower()
    if not key in __GLOBAL_CONFIGURATION:
        raise GConfigurationException(f'Unknown configuration key "{key}"')
    if subkey is None:
        return __GLOBAL_CONFIGURATION[key]
    subkey = subkey.lower()
    subconf = __GLOBAL_CONFIGURATION[key]
    if not subkey in subconf:
        raise GConfigurationException(f'Unknown configuration key "{key}.{subkey}"')
    return subconf[subkey]
