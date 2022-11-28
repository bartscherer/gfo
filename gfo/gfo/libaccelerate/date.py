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
__version__ = "1.1"

from datetime import datetime
from pytz import timezone, UTC
from typing import Union
from tzlocal import get_localzone_name

class ACDate(object):

    @staticmethod
    def date_to_string(date: datetime, date_format: str = '%d.%m.%y %H:%M:%S') -> str:
        return date.strftime(date_format)

    @staticmethod
    def local(timezone_identifier: Union[None, str] = None) -> datetime:
        if timezone_identifier is None:
            timezone_identifier = get_localzone_name()
        return ACDate.utc().astimezone(timezone(timezone_identifier))

    @staticmethod
    def local_timezone() -> str:
        return get_localzone_name()

    @staticmethod
    def utc() -> datetime:
        return datetime.now(tz=UTC)
