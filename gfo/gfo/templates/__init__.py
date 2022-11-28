from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from gfo.config import Constants
from gfo.exceptions.templates import GTemplateRenderingException
from gfo.libaccelerate.exception import excstr

__TEMPLATES = Jinja2Templates(
    directory=Constants.Environment.TEMPLATE_FILES_PATH
)

def template_to_response(*args, **kwargs) -> _TemplateResponse:
    if len(args) < 1 or not isinstance(args[0], str):
        raise GTemplateRenderingException(
            'The first argument has to be a string containing the template filename and should not be named.'
        )
    try:
        kwargs['Constants'] = Constants
        template_basename = args[0]
        return __TEMPLATES.TemplateResponse(
            template_basename,
            kwargs
        )
    except Exception as exc:
        raise GTemplateRenderingException(
            f'Failed to render template {args[0]}. {excstr(exc)}'
        )
