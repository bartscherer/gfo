from json import load
from os import listdir
from os.path import join, splitext
from typing import Union

from gfo.config import Constants

__GLOBAL_I18N: Union[dict, None] = None

def i18n() -> dict:
    global __GLOBAL_I18N
    if __GLOBAL_I18N is None:
        i18n = {}
        for file in listdir(Constants.Environment.I18N_PATH):
            if file.endswith('.json'):
                with open(join(Constants.Environment.I18N_PATH, file), 'rb') as translation_file:
                    i18n[splitext(file)[0].lower()] = load(translation_file)
        __GLOBAL_I18N = i18n
    return __GLOBAL_I18N

def get_i18n_language_from_string(language: Union[str, None]) -> str:
    if not isinstance(language, str):
        return Constants.Misc.I18N_DEFAULT_LANG
    if language.lower() in i18n():
        return language.lower()
    return Constants.Misc.I18N_DEFAULT_LANG