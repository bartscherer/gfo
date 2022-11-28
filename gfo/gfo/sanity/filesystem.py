from os import listdir
from typing import Any, Union

from gfo.exceptions import excstr
from gfo.sanity.datatypes import sanitize_str

def sanitize_path_readable_file(value: Any, **kwargs) -> tuple[Union[int, None], bool, Union[str, None]]:
    value, valid, errmsg = sanitize_str(value=value, **kwargs)
    if not valid:
        return value, valid, errmsg
    try:
        with open(value, 'rb') as test:
            test.close()
    except Exception as exc:
        return None, False, f'Failed to open path "{value}" in "rb" mode. {excstr(exc)}'
    return value, True, None

def sanitize_path_writable_file(value: Any, **kwargs) -> tuple[Union[int, None], bool, Union[str, None]]:
    value, valid, errmsg = sanitize_str(value=value, **kwargs)
    if not valid:
        return value, valid, errmsg
    try:
        with open(value, 'ab') as test:
            test.close()
    except Exception as exc:
        return None, False, f'Failed to open path "{value}" in "rb" mode. {excstr(exc)}'
    return value, True, None

def sanitize_path_readable_dir(value: Any, **kwargs) -> tuple[Union[int, None], bool, Union[str, None]]:
    value, valid, errmsg = sanitize_str(value=value, **kwargs)
    if not valid:
        return value, valid, errmsg
    try:
        listdir(value)
    except Exception as exc:
        return None, False, f'Failed to list contents of directory "{value}". {excstr(exc)}'
    return value, True, None