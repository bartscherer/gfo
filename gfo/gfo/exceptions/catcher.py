from traceback import format_exception

from gfo.config import Constants
from gfo.libaccelerate.exception import ac_excepthook_add_subscription
from gfo.libaccelerate.helpers import get_id
from gfo.logging import get_logger

__GLOBAL_UNHANDLED_EXCEPTION_HANDLER = None

class _UnhandledExceptionCatcher(object):

    def __init__(self) -> None:
        ac_excepthook_add_subscription(
            subscription_name=Constants.Internal.EXCEPTION_HOOK_NAME,
            callback_function=self.catch_exception
        )

    def catch_exception(self, exctype, value, traceback):
        exception_id = get_id(16)
        log = get_logger()
        log.error(f'ExceptionCatcher - caught an unexpected exception [id={exception_id}]')
        log.error(f'Exception: {exctype.__class__.__name__}: {value} [id={exception_id}]')
        log.error(f'''Traceback: {format_exception(
            exctype,
            value,
            traceback
        )}''')

def get_unhandled_exception_handler() -> _UnhandledExceptionCatcher:
    global __GLOBAL_UNHANDLED_EXCEPTION_HANDLER
    if __GLOBAL_UNHANDLED_EXCEPTION_HANDLER is None:
        __GLOBAL_UNHANDLED_EXCEPTION_HANDLER = _UnhandledExceptionCatcher()
    return __GLOBAL_UNHANDLED_EXCEPTION_HANDLER
