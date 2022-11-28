from os import mkdir, remove
from os.path import isdir, join as join_path
from shutil import rmtree

from gfo.config import from_config, Constants
from gfo.logging import get_logger

log = get_logger()

log.info(f'Running GFO version {Constants.Versioning.VERSION} - a software by {Constants.Versioning.AUTHOR}')

log.info('Executing prestart actions now...')

font_cache_dir = from_config('misc', 'font_cache_dir')
if isdir(font_cache_dir):
    log.info(f'The font cache directory "{font_cache_dir}" already exists. Removing it now...')
    rmtree(font_cache_dir)

log.info(f'Creating font cache directory "{font_cache_dir}"...')
mkdir(font_cache_dir)
log.info(f'Font cache directory "{font_cache_dir}" created!')

font_cache_test_path = join_path(font_cache_dir, '.test')
with open(font_cache_test_path, 'wb') as test:
    test.close()
remove(font_cache_test_path)
log.info(f'Write test to path "{font_cache_test_path}" succeeded')

ipc_dir = join_path(from_config('misc', 'font_cache_dir'), Constants.Internal.IPC_DIR_NAME)
if isdir(ipc_dir):
    log.info(f'IPC directory "{ipc_dir}" exists. Re-creating it now...')
    rmtree(ipc_dir)
    mkdir(ipc_dir)
else:
    log.info(f'IPC directory "{ipc_dir}" does not exist. Creating it now...')
    mkdir(ipc_dir)
log.info('Done')