from fastapi import HTTPException, status as status_codes
from os.path import dirname, join as join_path
from pathlib import Path

class Environment(object):

    '''
        Environment related constants (e.g. the gfo root directory)
    '''

    __this_dir = dirname(__file__)
    __parent_dir = Path(__this_dir).parent.absolute()
    ROOT_DIR: str = str(Path(__parent_dir).parent.absolute())
    CONFIG_FILE_PATH: str = join_path(ROOT_DIR, 'gfo.yaml')
    I18N_PATH: str = join_path(ROOT_DIR, 'i18n')
    STATIC_FILES_PATH: str = join_path(ROOT_DIR, 'static')
    TEMPLATE_FILES_PATH: str = join_path(ROOT_DIR, 'templates')

class HTTPErrors(object):

    '''
        Global error messages
    '''

    BAD_REQUEST = HTTPException(
        status_code=status_codes.HTTP_400_BAD_REQUEST,
        detail=f'The Google Fonts API responded with a HTTP 400 status code to your '
               f'request - please check your parameters.'
    )

    NOT_FOUND = HTTPException(
        status_code=status_codes.HTTP_404_NOT_FOUND,
        detail=f'The requested resource was not found.'
    )

    INTERNAL_SERVER_ERROR: HTTPException = HTTPException(
        status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='An internal server error occured while processing your request.'
    )

class Internal(object):

    '''
        Internal constants defining e.g. names of system exception
        hook subscriptions etc.
    '''

    EXCEPTION_HOOK_NAME: str = 'gfo_global_exceptions'
    IPC_DIR_NAME: str = '.ipc'
    SERVICE_INTERVAL_CACHE_CLEANUP: int = 60
    SERVICE_INTERVAL_DEFAULT: int = 900
    WORKER_ROLE_LEADER: str = 'leader'
    WORKER_ROLE_FOLLOWER: str = 'follower'

class Misc(object):

    '''
        Miscellaneous constants
    '''
    I18N_DEFAULT_LANG: str = 'de'

class Routing(object):

    '''
        Routing related constants e.g. route of the static files path
    '''

    STATIC_FILES_PATH: str = '/static'

class Versioning(object):

    '''
        Versioning related constants
    '''

    AUTHOR: str = 'Bartscherer Software <info@bartscherer.io>'
    VERSION: str = '1.0.0'

class Constants(object):

    '''
        A front-end to access the constants related to different
        topics (e.g. environment, paths, etc.)
    '''

    Environment: Environment = Environment()
    HTTPErrors: HTTPErrors = HTTPErrors()
    Internal: Internal = Internal()
    Misc: Misc = Misc()
    Routing: Routing = Routing()
    Versioning: Versioning = Versioning()
