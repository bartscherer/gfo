from json import loads
from os import getpid, listdir
from os.path import isfile, join as join_path
from random import randint
from sys import argv
from time import sleep
from typing import Union

from gfo.config import Constants, from_config
from gfo.exceptions import excstr
from gfo.exceptions.ipc import GIPCException
from gfo.libaccelerate.subprocess import ac_run_subprocess_shell
from gfo.logging import get_logger

__GLOBAL_WORKER_ROLE = None

def get_worker_amount() -> int:
    log = get_logger()
    next_arg_is_worker_amount = False
    for arg in argv:
        if next_arg_is_worker_amount:
            log.debug(
                f'This argument\'s value is "{arg}" so I assume that there are '
                f'{arg} workers running.'
            )
            return int(arg)
        if arg.lower() in ('-w', '--workers'):
            log.debug(
                f'Found argument "{arg}" in CLI arguments. '
                f'Assuming the next argument is the amount of workers.'
            )
            next_arg_is_worker_amount = True

    log.info(
        f'Failed to get worker amount via the -w/--workers CLI argument. '
        f'Attempting to determine them via a configuration file param now...'
    )

    next_arg_is_config_file = False
    for arg in argv:
        if next_arg_is_config_file:
            log.debug(
                f'This argument\'s value is "{arg}" so I will try to execute '
                f'the configuration file to get the worker amount via its output.'
            )
            for possible_interpreter in ('python', 'python3'):
                command = f'{possible_interpreter} "{arg}"'
                log.debug(f'Executing "{command}" to fetch the configuration output JSON')
                try:
                    result = ac_run_subprocess_shell(command)
                    log.debug(f'STDOUT: {result.stdout}')
                    log.debug(f'STDERR: {result.stderr}')
                    stdout_json = loads(result.stdout)
                    log.debug(f'Successfully parsed the STDOUT as JSON')
                    if 'workers' in stdout_json:
                        num_workers = stdout_json["workers"]
                        log.debug(
                            f'Found a key "workers" in the JSON. Its value is "{num_workers}" '
                            f'so I assume there are {num_workers} workers.'
                        )
                        return int(num_workers)
                except Exception as exc:
                    log.debug(
                        f'Failed to get the worker amount by executing the FastAPI '
                        f'gunicorn configuration file. {excstr(exc)}'
                    )
                break
        if arg.lower() in ('-c', '--config'):
            log.debug(
                f'Found argument "{arg}" in CLI arguments. '
                f'Assuming the next argument is the configuration file.'
            )
            next_arg_is_config_file = True
    log.error(
        'Failed to determine the amount of workers via the CLI params.'
    )
    raise GIPCException(
        f'Failed to determine how many workers there are '
        f'via the gunicorn command line parameters'
    )

def _get_worker_role() -> Union[Constants.Internal.WORKER_ROLE_FOLLOWER, Constants.Internal.WORKER_ROLE_LEADER]:
    log = get_logger()
    ipc_dir = join_path(from_config('misc', 'font_cache_dir'), Constants.Internal.IPC_DIR_NAME)
    my_pid = str(getpid())
    ipc_file = join_path(ipc_dir, my_pid)
    worker_amount = get_worker_amount()
    if worker_amount < 2:
        log.debug(f'I am the only worker so I\'m assuming I\'m leading.')
        return Constants.Internal.WORKER_ROLE_LEADER
    log.debug(f'Expecting {worker_amount} workers. Writing my IPC file now...')
    while 1:
        if isfile(ipc_file):
            log.debug(
                f'IPC file "{ipc_file}" exists. '
                f'Waiting for {worker_amount-1} more IPC files'
            )
            sleep(randint(0, 100) * 0.01)
            worker_pids = [int(f) for f in listdir(ipc_dir) if isfile(join_path(ipc_dir, f))]
            log.debug(
                f'Current worker PIDs: {worker_pids}'
            )
            if len(worker_pids) == worker_amount:
                log.debug(
                    'All worker PIDs are present. Exiting IPC now...'
                )
                break
        else:
            log.debug(f'IPC file "{ipc_file}" does not exist. creating it')
            with open(ipc_file, 'w') as ipc_fd:
                ipc_fd.close()
    if min(worker_pids) == int(my_pid):
        return Constants.Internal.WORKER_ROLE_LEADER
    else:
        return Constants.Internal.WORKER_ROLE_FOLLOWER

def get_worker_role() -> None:
    global __GLOBAL_WORKER_ROLE
    if __GLOBAL_WORKER_ROLE is None:
        __GLOBAL_WORKER_ROLE = _get_worker_role()
    return __GLOBAL_WORKER_ROLE
