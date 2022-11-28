from os import listdir, remove
from os.path import getmtime, isfile, join as join_path
from time import time

from gfo.config import Constants, from_config
from gfo.services.interface import Service
from gfo.services.service_manager import ServiceManager

class CacheCleanupService(Service):

    service_interval = Constants.Internal.SERVICE_INTERVAL_CACHE_CLEANUP
    service_name = 'CacheCleanup'

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager
        if hasattr(super(), 'service_name'):
            super().__init__(service_manager=service_manager)

    def run(self) -> None:
        cache_lifespan_seconds = from_config('misc', 'cache_lifespan_seconds')
        font_cache_dir = from_config('misc', 'font_cache_dir')
        for file in listdir(font_cache_dir):
            file_path = join_path(font_cache_dir, file)
            if not isfile(file_path):
                continue
            file_lifespan = int(time() - getmtime(file_path))
            if file_lifespan > cache_lifespan_seconds:
                self.log_debug(
                    f'Removing file "{file_path}" due to its lifespan '
                    f'exceeding the max cache lifespan ({file_lifespan} > '
                    f'{cache_lifespan_seconds})'
                )
                remove(file_path)
                self.log_debug(f'Removed file "{file_path}"')
            else:
                self.log_debug(
                    f'File "{file_path}" is still valid in cache. '
                    f'({file_lifespan}s <= {cache_lifespan_seconds}s)'
                )
