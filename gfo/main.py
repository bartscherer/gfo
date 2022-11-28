from fastapi import FastAPI, Request, Response, Query
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.routing import Mount
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from logging import getLogger
from os.path import isfile
from starlette.templating import _TemplateResponse
from typing import Optional, Union

from gfo.asgi_apps.static_files import static_files_app
from gfo.config import Constants, from_config
from gfo.exceptions import excstr
from gfo.exceptions.catcher import get_unhandled_exception_handler
from gfo.exceptions.googlefonts import GGoogleFontsBadRequestException, GGoogleFontsException
from gfo.googlefonts.downloader import GoogleFontsDownloader, get_google_fonts_downloader
from gfo.i18n import i18n, get_i18n_language_from_string
from gfo.ipc import get_worker_role
from gfo.libaccelerate.helpers import get_id, current_function_name
from gfo.logging import get_logger
from gfo.services import get_service_manager
from gfo.templates import template_to_response

'''
    Disable the uvicorn logger to prevent logging IP addresses
'''

uvicorn_access = getLogger('uvicorn.access')
uvicorn_access.disabled = True

'''
    Initialize the global exception handler
'''
get_unhandled_exception_handler()

'''
    Instantiate logger
'''
log = get_logger()

'''
    Get worker role
'''

log.info('Getting my worker role...')
if get_worker_role() == Constants.Internal.WORKER_ROLE_LEADER:
    log.info('This worker is the LEADER')
    svc_mngr = get_service_manager()
    svc_mngr.start_services()
    log.info('Started the service manager')
else:
    log.info('This worker is a follower')

'''
    Mount all apps
'''
routes = [
    Mount(
        path=Constants.Routing.STATIC_FILES_PATH,
        app=static_files_app,
        name=Constants.Routing.STATIC_FILES_PATH[1:]
    ),
]

'''
    Add all middlewares
'''
middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=from_config('cors', 'origins'),
        allow_methods=from_config('cors', 'allowed_methods'),
        allow_headers=from_config('cors', 'allowed_headers'),
        allow_credentials=from_config('cors', 'allow_credentials')
    ),
]

'''
    Instantiate FastAPI
'''
app = FastAPI(
    routes=routes,
    middleware=middlewares
)

@app.get(
    path='/',
    response_class=_TemplateResponse
)
def index(
    req: Request,
    language: Optional[str] = Query(default=Constants.Misc.I18N_DEFAULT_LANG)
) -> _TemplateResponse:
    log = get_logger()
    i18n_lang = get_i18n_language_from_string(language)
    try:
        return template_to_response(
            'index.html.j2',
            request=req,
            i18n=i18n()[i18n_lang]['index'],
            i18n_languages=i18n()[i18n_lang]['languages'],
            imprint_url=from_config('customization', 'imprint_url'),
            privacy_url=from_config('customization', 'privacy_url')
        )
    except Exception as exc:
        log.error(
            f'An unexpected exception occured while processing request. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.INTERNAL_SERVER_ERROR

@app.get(
    path='/css',
    responses={
        200: dict(
            content={
                'text/css': dict(
                    example='@font-face...'
                ),
                'application/json': None
            },
            description='The CSS style sheet with replaced font locations',
        ),
        400: dict(
            description='Google\'s API responded with HTTP 400. Check your params.',
        ),
        500: dict(
            description='An internal server error happened',
        )
    }
)
def get_font_via_gfonts_css_api(
    family: str = Query(),
    display: Optional[Union[str, None]] = Query(default=None),
    text: Optional[Union[str, None]] = Query(default=None),
    subset: Optional[Union[str, None]] = Query(default=None)
) -> Response:
    reqid = get_id(6)
    g : GoogleFontsDownloader = get_google_fonts_downloader()
    try:
        return Response(
            content=g.download_via_css_api(
                families_as_string=family,
                display=display,
                text=text,
                subset=subset,
                reqid=reqid
            ),
            media_type='text/css'
        )
    except GGoogleFontsBadRequestException as exc:
        log.warn(
            f'Google\'s API responded with a status of 400 to our font request. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.BAD_REQUEST
    except GGoogleFontsException as exc:
        log.error(
            f'An unexpected exception occured while downloading a font. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.INTERNAL_SERVER_ERROR
    except Exception as exc:
        log.error(
            f'An unexpected exception occured while processing request. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.INTERNAL_SERVER_ERROR

@app.get(
    path='/css2',
    responses={
        200: dict(
            content={
                'text/css': dict(
                    example='@font-face...'
                ),
                'application/json': None
            },
            description='The CSS style sheet with replaced font locations',
        ),
        400: dict(
            description='Google\'s API responded with HTTP 400. Check your params.',
        ),
        500: dict(
            description='An internal server error happened',
        )
    }
)
def get_font_via_gfonts_css2_api(
    family: list[str] = Query(),
    display: Optional[Union[str, None]] = Query(default=None),
    text: Optional[Union[str, None]] = Query(default=None),
) -> Response:
    reqid = get_id(6)
    g : GoogleFontsDownloader = get_google_fonts_downloader()
    try:
        return Response(
            content=g.download_via_css2_api(
                families=family,
                display=display,
                text=text,
                reqid=reqid
            ),
            media_type='text/css'
        )
    except GGoogleFontsBadRequestException as exc:
        log.warn(
            f'Google\'s API responded with a status of 400 to our font request. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.BAD_REQUEST
    except GGoogleFontsException as exc:
        log.error(
            f'An unexpected exception occured while downloading a font. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.INTERNAL_SERVER_ERROR
    except Exception as exc:
        log.error(
            f'An unexpected exception occured while processing request. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.INTERNAL_SERVER_ERROR

@app.get(
    path='/download/css',
    responses={
        200: dict(
            content={
                'application/octet-stream': dict(
                    example='The archive as bytes'
                ),
                'application/json': None
            },
            description='The archive (currently only zip) containing the rewritten CSS and font files (as application/octet-stream)',
        ),
        400: dict(
            description='Google\'s API responded with HTTP 400. Check your params.',
        ),
        500: dict(
            description='An internal server error happened',
        )
    }
)
def download_font_bundle_via_gfonts_css_api(
    family: str = Query(),
    display: Optional[Union[str, None]] = Query(default=None),
    text: Optional[Union[str, None]] = Query(default=None),
    subset: Optional[Union[str, None]] = Query(default=None)
) -> Response:
    reqid = get_id(6)
    bundle_archive_format = 'zip' # make this variable?
    g : GoogleFontsDownloader = get_google_fonts_downloader()
    try:
        bundle_bytes_io : BytesIO = g.download_via_css_api(
            families_as_string=family,
            display=display,
            text=text,
            subset=subset,
            reqid=reqid,
            download_as_bundle=True,
            bundle_archive_format=bundle_archive_format
        )
        return StreamingResponse(
            content=bundle_bytes_io,
            media_type='application/octet-stream',
            headers={
                'content-disposition': f'attachment; filename=gfo-bundle.{bundle_archive_format}'
            }
        )
    except GGoogleFontsBadRequestException as exc:
        log.warn(
            f'Google\'s API responded with a status of 400 to our font request. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.BAD_REQUEST
    except GGoogleFontsException as exc:
        log.error(
            f'An unexpected exception occured while downloading a font. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.INTERNAL_SERVER_ERROR
    except Exception as exc:
        log.error(
            f'An unexpected exception occured while processing request. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.INTERNAL_SERVER_ERROR

@app.get(
    path='/download/css2',
    responses={
        200: dict(
            content={
                'application/octet-stream': dict(
                    example='The archive as bytes'
                ),
                'application/json': None
            },
            description='The archive (currently only zip) containing the rewritten CSS and font files (as application/octet-stream)',
        ),
        400: dict(
            description='Google\'s API responded with HTTP 400. Check your params.',
        ),
        500: dict(
            description='An internal server error happened',
        )
    }
)
def download_font_bundle_via_gfonts_css2_api(
    family: list[str] = Query(),
    display: Optional[Union[str, None]] = Query(default=None),
    text: Optional[Union[str, None]] = Query(default=None),
) -> Response:
    reqid = get_id(6)
    bundle_archive_format = 'zip' # make this variable?
    g : GoogleFontsDownloader = get_google_fonts_downloader()
    try:
        bundle_bytes_io : BytesIO = g.download_via_css2_api(
            families=family,
            display=display,
            text=text,
            reqid=reqid,
            download_as_bundle=True,
            bundle_archive_format=bundle_archive_format
        )
        return StreamingResponse(
            content=bundle_bytes_io,
            media_type='application/octet-stream',
            headers={
                'content-disposition': f'attachment; filename=gfo-bundle.{bundle_archive_format}'
            }
        )
    except GGoogleFontsBadRequestException as exc:
        log.warn(
            f'Google\'s API responded with a status of 400 to our font request. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.BAD_REQUEST
    except GGoogleFontsException as exc:
        log.error(
            f'An unexpected exception occured while downloading a font. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.INTERNAL_SERVER_ERROR
    except Exception as exc:
        log.error(
            f'An unexpected exception occured while processing request. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.INTERNAL_SERVER_ERROR

@app.get(
    path='/font/{font_url_md5}',
    responses={
        200: dict(
            content={
                'application/octet-stream': dict(
                    example='The font file as bytes'
                ),
                'application/json': None
            },
            description='The archive containing the rewritten CSS and font files',
        ),
        404: dict(
            description='The requested font file does not exist'
        ),
        500: dict(
            description='An internal server error happened',
        )
    }
)
def get_font_from_local_storage(req: Request, font_url_md5: str) -> Response:
    g = GoogleFontsDownloader()
    font_path = g.get_font_path_from_md5(font_url_md5)
    if not isfile(font_path):
        raise Constants.HTTPErrors.NOT_FOUND
    try:
        return FileResponse(
            path=font_path,
            media_type='application/octet-stream',
            content_disposition_type='attachment'
        )
    except Exception as exc:
        log.error(
            f'An unexpected exception occured while processing request. '
            f'[endpoint={current_function_name()}] {excstr(exc)}'
        )
        raise Constants.HTTPErrors.INTERNAL_SERVER_ERROR