from typing import Any, Callable, Union

from gfo.exceptions import excstr
from gfo.exceptions.sanity import GSanitizerInvalidException
from gfo.sanity.datatypes import (
    sanitize_bool,
    sanitize_dict,
    sanitize_float,
    sanitize_int,
    sanitize_list,
    sanitize_str,
    sanitize_tuple
)
from gfo.sanity.filesystem import (
    sanitize_path_readable_dir,
    sanitize_path_readable_file,
    sanitize_path_writable_file
)
from gfo.sanity.timezone import sanitize_timezone

class Sanitizers(object):
    bool = sanitize_bool
    dict = sanitize_dict
    float = sanitize_float
    int = sanitize_int
    list = sanitize_list
    str = sanitize_str
    tuple = sanitize_tuple
    path_readable_dir = sanitize_path_readable_dir
    path_readable_file = sanitize_path_readable_file
    path_writable_file = sanitize_path_writable_file
    timezone = sanitize_timezone

def sanitize(value: Any, sanitizer: Callable, **kwargs) -> tuple[bool, Any, Union[str, None]]:
    try:
        return sanitizer(value, **kwargs)
    except Exception as exc:
        raise GSanitizerInvalidException(
            f'Failed to validate the given value using sanitizer method '
            f'{sanitizer.__name__ if hasattr(sanitizer, "__name__") else "[unknown]"} '
            f'{excstr(exc)}'
        )
