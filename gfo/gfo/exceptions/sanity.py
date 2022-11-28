class GSanitizerInvalidException(Exception):
    '''
        This exception gets thrown when there is an invalid 
        sanitizing method that raises an exception instead of
        returning an error message etc.
    '''
    pass
