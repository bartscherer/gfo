'''
MIT License

Copyright (c) 2022 Thomas Bartscherer <thomas@bartscherer.io>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys
from time import sleep
from typing import Callable

global ___ac_excepthook_subscriptions___
if not '___ac_excepthook_subscriptions___' in globals():
    ___ac_excepthook_subscriptions___ = {}

def __ac_except_hook(exctype, value, traceback, called_hooks = None):
    global ___ac_excepthook_subscriptions___
    if called_hooks is None:
        called_hooks = []
    try:
        for subscription in ___ac_excepthook_subscriptions___:
            if subscription in called_hooks:
                continue
            try:
                ___ac_excepthook_subscriptions___[subscription](exctype, value, traceback)
                called_hooks.append(subscription)
            except:
                pass
    except RuntimeError as exc: # subscriptions changed during processing
        sleep(.01)
        __ac_except_hook(exctype, value, traceback, called_hooks)
    sys.__excepthook__(exctype, value, traceback)

sys.excepthook = __ac_except_hook

def ac_excepthook_add_subscription(subscription_name: str, callback_function: Callable) -> None:
    global ___ac_excepthook_subscriptions___
    ___ac_excepthook_subscriptions___[subscription_name] = callback_function

def ac_excepthook_del_subscription(subscription_name: str) -> None:
    global ___ac_excepthook_subscriptions___
    del ___ac_excepthook_subscriptions___[subscription_name]

def excstr(exc: Exception) -> str:

    '''
        Method which creates a human readable
        exception description out of a generic
        exception object. It also provides info
        about filename, line number, etc.
    '''

    _, _, exc_tb = sys.exc_info()
    if exc.__class__.__name__ == 'HTTPException':
        try:
            return f'[{exc.__class__.__name__}: detail={exc.detail};status={exc.status_code}]'
        except Exception as exc:
            pass
    if exc_tb is None:
        return f'[{exc.__class__.__name__}: {exc}]'
    exc_traceback_frame = exc_tb.tb_frame
    line_number = exc_tb.tb_lineno
    exc_file = exc_traceback_frame.f_code.co_filename
    return f'[{exc.__class__.__name__}: {exc} | {exc_file};line:{line_number}]'

class ACLockException(Exception):
    pass

class ACLogException(Exception):
    pass

class ACSubprocessException(Exception):
    pass
