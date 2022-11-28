class GIPCException(Exception):
    '''
        This exception gets thrown when some problems
        in the interprocess communication happens.
        E.g. a worker is unable to determine how many
        workers there are besides it.
    '''
    pass