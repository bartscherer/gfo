from time import sleep

from gfo.logging import get_logger
from gfo.services import get_service_manager

log = get_logger()
log.info('Starting the service manager...')
svc_mngr = get_service_manager()
svc_mngr.start_services()
log.info('Started the service manager successfully')
while(1):
    try:
        sleep(.1)
    except KeyboardInterrupt:
        break
log.info('Service manager exiting...')
exit(0)