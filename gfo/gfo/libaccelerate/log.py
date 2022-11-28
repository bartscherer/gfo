'''
MIT License

Copyright (c) 2022 Thomas Bartscherer <thomas@bartscherer.io>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

__author__ = "Thomas Bartscherer <thomas@bartscherer.io>"
__copyright__ = "Copyright (C) 2022 Thomas Bartscherer <thomas@bartscherer.io>"
__license__ = "MIT"
__version__ = "1.0"

from colorama import (
    Fore,
    Style,
    init as init_colorama
)
from fcntl import flock, LOCK_EX, LOCK_UN
from os import getpid
from sys import stdout
from typing import Union
from gfo.libaccelerate.date import ACDate
from gfo.libaccelerate.exception import (
    ac_excepthook_add_subscription,
    excstr,
    ACLogException
)
from gfo.libaccelerate.lock import (
    ac_lock,
    ac_unlock
)

class ACLogConfiguration(object):

    levels = {
        'error': {
            'color': Fore.LIGHTRED_EX,
            'color_whole_line': True,
            'enabled': True,
            'label': 'error',
        },
        'warn': {
            'color': Fore.LIGHTYELLOW_EX,
            'color_whole_line': True,
            'enabled': True,
            'label': 'warning'
        },
        'info': {
            'color': Fore.LIGHTGREEN_EX,
            'color_whole_line': False,
            'enabled': True,
            'label': 'info'
        },
        'debug': {
            'color': Fore.LIGHTBLACK_EX,
            'color_whole_line': False,
            'enabled': False,
            'label': 'debug'
        },
    }

    def __init__(self) -> None:
        self.log_catch_unexpected_errors: bool = True
        self.log_colors_enabled: bool = True
        self.log_file: Union[None, str] = None
        self.log_include_pid: bool = False
        self.log_timezone = ACDate.local_timezone()

    def set_log_level_enabled(self, level: str, enabled: bool) -> None:
        self.levels[level]['enabled'] = enabled

    @property
    def log_enable_debug(self) -> bool:
        return self.levels['debug']['enabled']

    @log_enable_debug.setter
    def log_enable_debug(self, enabled: bool) -> None:
        self.set_log_level_enabled('debug', enabled=enabled)

    @property
    def log_enable_info(self) -> bool:
        return self.levels['info']['enabled']

    @log_enable_info.setter
    def log_enable_info(self, enabled: bool) -> None:
        self.set_log_level_enabled('info', enabled=enabled)

    @property
    def log_enable_warn(self) -> bool:
        return self.levels['warn']['enabled']

    @log_enable_warn.setter
    def log_enable_warn(self, enabled: bool) -> None:
       self.set_log_level_enabled('warn', enabled=enabled)

    @property
    def log_enable_error(self) -> bool:
        return self.levels['error']['enabled']

    @log_enable_error.setter
    def log_enable_error(self, enabled: bool) -> None:
        self.set_log_level_enabled('error', enabled=enabled)

class ACLog(object):
    def __init__(self, log_configuration: ACLogConfiguration) -> None:
        self.config = log_configuration
        self.logfile = None
        self.lock_name = '__ac_logger_lock__'
        self.subscription_name = '__ac_logger_excepthook_subscription__'
        if self.config.log_colors_enabled:
            init_colorama()
        if self.config.log_file is not None:
            try:
                self.logfile = open(self.config.log_file, 'ab')
            except Exception as exc:
                raise ACLogException(f'Failed to open log file "{self.config.log_file}" for writing. {excstr(exc)}')
        if self.config.log_catch_unexpected_errors:
            try:
                ac_excepthook_add_subscription(self.subscription_name, self.__process_unhandled_exception)
            except Exception as exc:
                raise ACLogException(f'Failed to add subscription to the system excepthook. {excstr(exc)}')

    def __process_unhandled_exception(self, exc_type, exc_msg, exc_tb) -> None:
        exc_traceback_frame = exc_tb.tb_frame
        line_number = exc_tb.tb_lineno
        exc_file = exc_traceback_frame.f_code.co_filename
        self.error(f'Unhandled exception occured [{exc_type.__name__}: {exc_msg} | {exc_file};line:{line_number}]')

    def __write_log(self, level: str, message: str) -> None:
        level_config = ACLogConfiguration.levels[level]
        if not level_config['enabled']:
            return
        ac_lock(self.lock_name)
        try:
            timestamp = ACDate.date_to_string(ACDate.local(self.config.log_timezone))
            label = level_config['label']
            if self.config.log_colors_enabled:
                color = level_config['color']
                color_whole_line = level_config['color_whole_line']
                msg = str(
                        f'{Style.BRIGHT}{Fore.LIGHTBLACK_EX}{timestamp}{Fore.RESET} '
                        f'[{color}{label}{"@" + str(getpid()) if self.config.log_include_pid else ""}{Fore.RESET}] '
                        f'{"" if not color_whole_line else color}{message}{Fore.RESET}\n'
                    )
                msg_file = f'{timestamp} [{label}] {message}\n'
            else:
                msg = msg_file =f'{timestamp} [{label}] {message}\n'
            stdout.write(msg)
            stdout.flush()
            if self.logfile is not None:
                flock(self.logfile, LOCK_EX)
                self.logfile.write(msg_file.encode('utf-8'))
                self.logfile.flush()
                flock(self.logfile, LOCK_UN)
        except Exception as exc:
            if self.config.log_enable_error:
                try:
                    print(f'[error] Logging message "{message}" failed. {excstr(exc)}')
                except:
                    pass
        ac_unlock(self.lock_name)

    def debug(self, message: str) -> None:
        self.__write_log('debug', message)

    def info(self, message: str) -> None:
        self.__write_log('info', message)

    def warn(self, message: str) -> None:
        self.__write_log('warn', message)

    def error(self, message: str) -> None:
        self.__write_log('error', message)
