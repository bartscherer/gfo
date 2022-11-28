from os.path import join as join_path

from gfo.config import Constants, from_config
from gfo.libaccelerate.log import ACLog, ACLogConfiguration

__GLOBAL_LOGGER = None

def get_logger() -> ACLog:
    global __GLOBAL_LOGGER
    if __GLOBAL_LOGGER is None:
        log_config = ACLogConfiguration()
        log_config.log_file = join_path(Constants.Environment.ROOT_DIR, from_config('log', 'file_path'))
        log_config.log_enable_debug = from_config('log', 'debug')
        log_config.log_enable_info = from_config('log', 'info')
        log_config.log_enable_warn = from_config('log', 'warn')
        log_config.log_enable_error = from_config('log', 'error')
        log_config.log_timezone = from_config('misc', 'timezone').zone
        log_config.log_catch_unexpected_errors = from_config('log', 'unexpected_exceptions')
        log_config.log_include_pid = True
        __GLOBAL_LOGGER = ACLog(log_configuration=log_config)
    return __GLOBAL_LOGGER
