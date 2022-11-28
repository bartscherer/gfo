from typing import Any, Union

def sanitize_str(value: Any, **kwargs) -> tuple[Union[str, None], bool, Union[str, None]]:
    if not isinstance(value, str):
        return None, False, f'The submitted input is not a string (type "{type(value).__name__}")'
    return value, True, None

def sanitize_int(value: Any, **kwargs) -> tuple[Union[int, None], bool, Union[str, None]]:
    if not isinstance(value, int):
        return None, False, f'The submitted input is not an integer (type "{type(value).__name__}")'
    return value, True, None

def sanitize_float(value: Any, **kwargs) -> tuple[Union[float, None], bool, Union[str, None]]:
    if not isinstance(value, float):
        if isinstance(value, int):
            return float(value), True, None
        return None, False, f'The submitted input is not a float (or an integer) (type "{type(value).__name__}")'
    return value, True, None

def sanitize_bool(value: Any, **kwargs) -> tuple[Union[bool, None], bool, Union[str, None]]:
    if not isinstance(value, bool):
        if isinstance(value, int):
            if value in (0, 1):
                return bool(value), True, None
        return None, False, f'The submitted input is not a boolean (type "{type(value).__name__}")'
    return value, True, None

def sanitize_tuple(value: Any, **kwargs) -> tuple[Union[tuple, None], bool, Union[str, None]]:
    if not isinstance(value, tuple):
        return None, False, f'The submitted input is not a tuple (type "{type(value).__name__}")'
    return value, True, None

def sanitize_list(value: Any, **kwargs) -> tuple[Union[list, None], bool, Union[str, None]]:
    if not isinstance(value, list):
        return None, False, f'The submitted input is not a list (type "{type(value).__name__}")'
    return value, True, None

def sanitize_dict(value: Any, **kwargs) -> tuple[Union[dict, None], bool, Union[str, None]]:
    if not isinstance(value, dict):
        return None, False, f'The submitted input is not a dict (type "{type(value).__name__}")'
    return value, True, None