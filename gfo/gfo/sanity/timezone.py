from pytz import timezone
from typing import Any, Union

from gfo.sanity.datatypes import sanitize_str

def sanitize_timezone(value: Any, **kwargs) -> tuple[Union[timezone, None], bool, Union[str, None]]:
    value, valid, errmsg = sanitize_str(value)
    if not valid:
        return value, valid, errmsg
    try:
        return timezone(value), True, None
    except Exception as exc:
        return None, False, f'Invalid timezone identifier "{value}"'