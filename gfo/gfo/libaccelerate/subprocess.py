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

from subprocess import run

from gfo.libaccelerate.exception import (
    excstr,
    ACSubprocessException
)

class ACSubprocessResult(object):
    def __init__(
        self,
        rc: int,
        stderr: str,
        stdout: str
    ) -> None:
        self.rc = rc
        self.stderr = stderr
        self.stderr_lines = stderr.split('\n')
        self.stdout = stdout
        self.stdout_lines = stdout.split('\n')

def ac_run_subprocess(command: list, args: list, timeout: float = 60.0) -> ACSubprocessResult:
    try:
        full_command = [command] + args
        proc = run(
            full_command,
            capture_output=True,
            encoding='utf-8',
            timeout=timeout,
        )
    except Exception as exc:
        raise ACSubprocessException(f'Failed to execute subprocess "{" ".join(full_command)}". {excstr(exc)}')
    sr = ACSubprocessResult(
        rc = proc.returncode,
        stderr = proc.stderr,
        stdout = proc.stdout
    )
    return sr

def ac_run_subprocess_shell(command: str, timeout: float = 60.0) -> ACSubprocessResult:
    try:
        proc = run(
            command,
            capture_output=True,
            encoding='utf-8',
            shell=True,
            timeout=timeout,
        )
    except Exception as exc:
        raise ACSubprocessException(f'Failed to execute subprocess "{command}". {excstr(exc)}')
    sr = ACSubprocessResult(
        rc = proc.returncode,
        stderr = proc.stderr,
        stdout = proc.stdout
    )
    return sr
