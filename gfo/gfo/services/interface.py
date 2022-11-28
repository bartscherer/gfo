from time import sleep, time_ns
from typing import Any

from gfo.config import Constants
from gfo.exceptions import excstr

class Service(object):

    service_interval = Constants.Internal.SERVICE_INTERVAL_DEFAULT
    service_name = 'GenericService'

    def __init__(self, service_manager: Any):
        self.service_manager = service_manager
        if hasattr(super(), 'service_name'):
            super().__init__(service_manager=service_manager)

    def _run(self) -> None:
        while 1:
            t0 = time_ns()
            try:
                self.log_debug('Starting service execution...')
                self.run()
                self.log_debug(f'Successfully executed service tasks after ~{round((time_ns() - t0) / 1000**3, 4)} seconds')
            except Exception as exc:
                self.log_error(f'Failed to execute service tasks {excstr(exc)}')
            sleep(self.service_interval)

    def run(self) -> None:
        pass

    def log_debug(self, msg) -> None:
        self.service_manager.log_debug(msg, self)

    def log_info(self, msg) -> None:
        self.service_manager.log_info(msg, self)

    def log_warn(self, msg) -> None:
        self.service_manager.log_warn(msg, self)

    def log_error(self, msg) -> None:
        self.service_manager.log_error(msg, self)
