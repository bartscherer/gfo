from hashlib import md5 as hash_md5
from io import BytesIO
from os import mkdir, remove
from os.path import basename, getmtime, isdir, isfile, join as join_path
from requests import get as http_get
from shutil import copy as copy_file, make_archive, move
from tempfile import NamedTemporaryFile, TemporaryDirectory
from time import time
from typing import Union
from urllib.parse import urlencode, quote_plus

from gfo.config import from_config
from gfo.exceptions import excstr
from gfo.exceptions.googlefonts import GGoogleFontsException, GGoogleFontsBadRequestException
from gfo.libaccelerate.helpers import get_id
from gfo.logging import get_logger

def md5(s: str) -> str:
    return hash_md5(s.encode('utf-8') if isinstance(s, str) else s).hexdigest()

__GLOBAL_GOOGLE_FONTS_DOWNLOADER = None

class GoogleFontsDownloader(object):

    def __init__(self) -> None:
        self.storage_path = from_config('misc', 'font_cache_dir')
        self.storage_staging_path = join_path(self.storage_path, f'stage-{get_id(6)}')
        if not isdir(self.storage_path):
            try:
                mkdir(self.storage_path)
            except Exception as exc:
                raise GGoogleFontsException(
                    f'Failed to create font storage path "{self.storage_path}". {excstr(exc)}'
                )
        if not isdir(self.storage_staging_path):
            try:
                mkdir(self.storage_staging_path)
            except Exception as exc:
                raise GGoogleFontsException(
                    f'Failed to create font storage path "{self.storage_staging_path}". {excstr(exc)}'
                )

    def __download(self, from_url: str) -> str:
        try:
            req = http_get(url=from_url)
        except Exception as exc:
            raise GGoogleFontsException(
                f'Failed to download content from URL "{from_url}". {excstr(exc)}'
            )
        if req.status_code < 200 or req.status_code > 299:
            if req.status_code == 400:
                raise GGoogleFontsBadRequestException(
                    f'The received status code of the font at URL "{from_url}" '
                    f'was not in range 200-299. Received code: {req.status_code}'
                )
            raise GGoogleFontsException(
                f'The received status code of the font at URL "{from_url}" '
                f'was not in range 200-299. Received code: {req.status_code}'
            )
        return req.content

    def convert_rewritten_css_sheet_to_archive(
        self,
        rewritten_css_sheet: str,
        archive_format: str = 'zip'
    ) -> BytesIO:
        font_urls = []
        font_face_split = rewritten_css_sheet.split('@font-face')
        for font_face in font_face_split:
            if 'src:' in font_face:
                font_urls.append(font_face.split('url(')[1].split(')')[0])
        for font_url in font_urls:
            rewritten_css_sheet = rewritten_css_sheet.replace(font_url, f'./{font_url.split("/font/")[1]}')
        with TemporaryDirectory() as tmpdir:
            for font_url in font_urls:
                font_file_basename = font_url.split('/font/')[1]
                copy_file(join_path(self.storage_path, font_file_basename), tmpdir)
            with open(join_path(tmpdir, 'fonts.css'), 'wb') as font_css:
                font_css.write(rewritten_css_sheet.encode('utf-8'))
            archive_file = NamedTemporaryFile(prefix='gfo-bundle-', delete=True)
            archive_file_name = archive_file.name
            archive_file.close()
            make_archive(
                base_name=archive_file_name,
                format=archive_format,
                root_dir=tmpdir
            )
        final_archive_path = f'{archive_file_name}.{archive_format}'
        archive_bytes_io = BytesIO()
        with open(final_archive_path, 'rb') as arc:
            while 1:
                data = arc.read(4096)
                if not data:
                    break
                archive_bytes_io.write(data)
        archive_bytes_io.seek(0)
        remove(final_archive_path)
        return archive_bytes_io

    def download_via_css_api(
        self,
        families_as_string: str,
        display: Union[str, None],
        text: Union[str, None],
        subset: Union[str, None],
        reqid: str,
        download_as_bundle: bool = False,
        bundle_archive_format: str = 'zip'
    ) -> Union[str, BytesIO]:
        log = get_logger()
        google_fonts_url = 'https://fonts.googleapis.com/css?'
        google_fonts_url_params = [('family', families_as_string)]
        if display is not None:
            google_fonts_url_params.append(('display', display))
        if text is not None:
            google_fonts_url_params.append(('text', text))
        if subset is not None:
            google_fonts_url_params.append(('subset', subset))
        url = google_fonts_url + urlencode(google_fonts_url_params, quote_via=quote_plus)
        log.debug(f'[css] Retrieving font stylesheet from "{url}" [reqid={reqid}]')
        rewritten_css_sheet = self.store_locally_and_return_css(url=url, reqid=reqid)

        if download_as_bundle:
            return self.convert_rewritten_css_sheet_to_archive(
                rewritten_css_sheet=rewritten_css_sheet,
                archive_format=bundle_archive_format
            )

        return rewritten_css_sheet

    def download_via_css2_api(
        self,
        families: list[str],
        display: Union[str, None],
        text: Union[str, None],
        reqid: str,
        download_as_bundle: bool = False,
        bundle_archive_format: str = 'zip'
    ) -> Union[str, BytesIO]:
        log = get_logger()
        google_fonts_url = 'https://fonts.googleapis.com/css2?'
        google_fonts_url_params = [('family', family) for family in families]
        if display is not None:
            google_fonts_url_params.append(('display', display))
        if text is not None:
            google_fonts_url_params.append(('text', text))
        url = google_fonts_url + urlencode(google_fonts_url_params, quote_via=quote_plus)
        log.debug(f'[css2] Receiving font stylesheet from "{url}" [reqid={reqid}]')
        rewritten_css_sheet = self.store_locally_and_return_css(url=url, reqid=reqid)

        if download_as_bundle:
            return self.convert_rewritten_css_sheet_to_archive(
                rewritten_css_sheet=rewritten_css_sheet,
                archive_format=bundle_archive_format
            )

        return rewritten_css_sheet

    def get_font_path_from_md5(self, font_md5: str) -> str:
        return join_path(self.storage_path, font_md5)

    def store_locally_and_return_css(self, url: str, reqid: str) -> str:

        log = get_logger()

        css_path = join_path(self.storage_path, md5(url))

        perform_download = True

        if isfile(css_path):
            log.debug(f'Font CSS path "{css_path}" exists [reqid={reqid}]')
            if time() - getmtime(css_path) > from_config('misc', 'cache_lifespan_seconds'):
                log.debug(f'Font CSS file "{css_path}" exceeded its cache lifespan - removing it [reqid={reqid}]')
                remove(css_path)
            else:
                log.debug(f'Font CSS file is available cached at "{css_path}" [reqid={reqid}]')
                with open(css_path, 'rb') as css_file:
                    raw_css = css_file.read().decode('utf-8')
                perform_download = False

        if perform_download:
            log.debug(f'Downloading font CSS from "{url}" to "{css_path}" [reqid={reqid}]')
            raw_css = self.__download(from_url=url).decode('utf-8')
            with open(css_path, 'wb') as css_file:
                log.debug(f'Writing new font CSS to "{css_path}" [reqid={reqid}]')
                css_file.write(raw_css.encode('utf-8'))

        '''
            Extract font urls from css
        '''
        md5_to_font_urls = {}
        for part in raw_css.split('url('):
            if ')' in part:
                font_url = part.split(')')[0]
                log.debug(f'Extracted font URL "{font_url}" from font CSS from "{css_path}" [reqid={reqid}]')
                md5_to_font_urls[md5(font_url)] = font_url


        '''
            Download all font files that don't exist yet
        '''
        stage_files = []
        for font_url_md5 in md5_to_font_urls:
            url_font_path = join_path(self.storage_path, font_url_md5)
            url_font_staging_path = join_path(self.storage_staging_path, font_url_md5)
            if isfile(url_font_path):
                log.debug(f'Font file "{url_font_path}" exists [reqid={reqid}]')
                if time() - getmtime(url_font_path) > from_config('misc', 'cache_lifespan_seconds'):
                    log.debug(f'Font file "{url_font_path}" exceeded the cache lifespan [reqid={reqid}]')
                    remove(url_font_path)
                    with open(url_font_staging_path, 'wb') as font_file:
                        font_file.write(self.__download(md5_to_font_urls[font_url_md5]))
                    stage_files.append(url_font_staging_path)
            else:
                log.debug(f'Downloading font file "{url_font_path}" to "{url_font_staging_path}" [reqid={reqid}]')
                with open(url_font_staging_path, 'wb') as font_file:
                    font_file.write(self.__download(md5_to_font_urls[font_url_md5]))
                stage_files.append(url_font_staging_path)

        for staging_file_path in stage_files:
            log.debug(f'Moving font file "{staging_file_path}" to "{join_path(self.storage_path, basename(staging_file_path))}" [reqid={reqid}]')
            move(
                src=staging_file_path,
                dst=join_path(self.storage_path, basename(staging_file_path))
            )

        for md5url, url in md5_to_font_urls.items():
            raw_css = raw_css.replace(url, f'/font/{md5url}')

        return raw_css

def get_google_fonts_downloader() -> GoogleFontsDownloader:
    global __GLOBAL_GOOGLE_FONTS_DOWNLOADER
    if __GLOBAL_GOOGLE_FONTS_DOWNLOADER is None:
        __GLOBAL_GOOGLE_FONTS_DOWNLOADER = GoogleFontsDownloader()
    return __GLOBAL_GOOGLE_FONTS_DOWNLOADER
