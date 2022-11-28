from copy import deepcopy
from threading import Thread

from gfo.logging import get_logger
from gfo.services.interface import Service

class ServiceManager(object):

    def __init__(self, service_classes: tuple[Service]) -> None:
        self.__service_classes = service_classes
        self.__services = {}
        self.__service_threads = {}

    def log_debug(self, msg: str, service: Service) -> None:
        get_logger().debug(f'[{service.service_name}@ServiceManager] {msg}')

    def log_info(self, msg: str, service: Service) -> None:
        get_logger().info(f'[{service.service_name}@ServiceManager] {msg}')

    def log_warn(self, msg: str, service: Service) -> None:
        get_logger().warn(f'[{service.service_name}@ServiceManager] {msg}')

    def log_error(self, msg: str, service: Service) -> None:
        get_logger().error(f'[{service.service_name}@ServiceManager] {msg}')

    @property
    def service_threads(self):
        return deepcopy(self.__service_threads)

    def start_services(self) -> None:
        for service in self.__service_classes:
            self.__services[service.service_name] = service(self)
            self.__service_threads[service.service_name] = Thread(target=self.__services[service.service_name]._run)
            self.__service_threads[service.service_name].setDaemon(True)
            self.__service_threads[service.service_name].start()
