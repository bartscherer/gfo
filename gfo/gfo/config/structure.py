from pytz import timezone

from gfo.sanity import Sanitizers

'''
    This is the global configuration structure. The YAML file has to consist of a 
    mapping of keys:str that relate to a single topic to values:dict[str, Any].
'''

CONFIGURATION_STRUCTURE = dict(
    cors=dict(
        allow_credentials=dict(
            description='Whether the CORS middleware allows cookies in cross origin requests',
            default=True,
            sanitizer=Sanitizers.bool
        ),
        allowed_headers=dict(
            description='A list of allowed CORS headers',
            default=['*'],
            sanitizer=Sanitizers.list
        ),
        allowed_methods=dict(
            description='A list of allowed CORS HTTP methods',
            default=['*'],
            sanitizer=Sanitizers.list
        ),
        origins=dict(
            description='A list of allowed CORS origins',
            default=['*'],
            sanitizer=Sanitizers.list
        ),
    ),
    customization=dict(
        imprint_url=dict(
            description='The URL of your imprint',
            default='',
            sanitizer=Sanitizers.str
        ),
        privacy_url=dict(
            description='The URL of your privacy agreement',
            default='',
            sanitizer=Sanitizers.str
        )
    ),
    log=dict(
        file_path=dict(
            description='The log file path (relative to the directory where main.py resides)',
            default='gfo.log',
            sanitizer=Sanitizers.path_writable_file
        ),
        debug=dict(
            description='Whether to enable debug level logging',
            default=False,
            sanitizer=Sanitizers.bool
        ),
        info=dict(
            description='Whether to enable info level logging',
            default=True,
            sanitizer=Sanitizers.bool
        ),
        warn=dict(
            description='Whether to enable warning level logging',
            default=True,
            sanitizer=Sanitizers.bool
        ),
        error=dict(
            description='Whether to enable error level logging',
            default=True,
            sanitizer=Sanitizers.bool
        ),
        unexpected_exceptions=dict(
            description='Whether to log ALL unexpected exceptions (the global exception catcher should probably be enough)',
            default=False,
            sanitizer=Sanitizers.bool
        )
    ),
    misc=dict(
        cache_lifespan_seconds=dict(
            description='The amount of seconds until a cached font file expires',
            default=3600,
            sanitizer=Sanitizers.int
        ),
        font_cache_dir=dict(
            description='The directory to store the cached font files in',
            default='/tmp/fonts',
            sanitizer=Sanitizers.str
        ),
        timezone=dict(
            description='This host\'s timezone as a string (e.g. Europe/Berlin)',
            default=timezone('UTC'),
            sanitizer=Sanitizers.timezone
        )
    ),
)
