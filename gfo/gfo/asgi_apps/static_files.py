from fastapi.staticfiles import StaticFiles

from gfo.config import Constants

static_files_app = StaticFiles(
    directory=Constants.Environment.STATIC_FILES_PATH
)
