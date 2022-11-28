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

__author__ = "Thomas Bartscherer <thomas@bartscherer.io>"
__copyright__ = "Copyright (C) 2022 Thomas Bartscherer <thomas@bartscherer.io>"
__license__ = "MIT"
__version__ = "1.0"

from threading import Lock
from gfo.libaccelerate.exception import (
    excstr,
    ACLockException
)

global ___ac_common_locks___
if not '___ac_common_locks___' in globals():
    ___ac_common_locks___ = {}

def ac_lock(lock_name: str) -> None:
    if not lock_name in ___ac_common_locks___:
        ___ac_common_locks___[lock_name] = Lock()
    ___ac_common_locks___[lock_name].acquire()

def ac_unlock(lock_name: str) -> None:
    try:
        ___ac_common_locks___[lock_name].release()
    except RuntimeError as exc:
        pass
    except Exception as exc:
        raise ACLockException(f'Failed to get lock "{lock_name}". {excstr(exc)}')

