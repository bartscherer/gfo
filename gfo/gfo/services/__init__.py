from gfo.services.cache_cleanup import CacheCleanupService
from gfo.services.service_manager import ServiceManager

__GLOBAL_SERVICE_MANAGER = None

def get_all_service_classes() -> tuple:
    return (
        CacheCleanupService,
    )

def get_service_manager() -> ServiceManager:
    global __GLOBAL_SERVICE_MANAGER
    if __GLOBAL_SERVICE_MANAGER is None:
        __GLOBAL_SERVICE_MANAGER = ServiceManager(get_all_service_classes())
    return __GLOBAL_SERVICE_MANAGER
