import logging
from http import HTTPStatus
from typing import Callable, Awaitable, Optional, Mapping
from aiohttp.web_request import Request

from aiohttp import web
from aiohttp.web_exceptions import (
    HTTPBadRequest, HTTPException, HTTPInternalServerError,
)

from marshmallow import ValidationError

from app.api.payloads import JsonPayload

log = logging.getLogger(__name__)


def format_http_error(http_error_cls, message: Optional[str] = None,
                      fields: Optional[Mapping] = None) -> HTTPException:
    """
    Форматирует ошибку в виде HTTP исключения
    """
    status = HTTPStatus(http_error_cls.status_code)
    error = {
        'code': status.name.lower(),
        'message': message or status.description
    }

    if fields:
        error['fields'] = fields

    return http_error_cls(body={'error': error})


def handle_validation_error(error: ValidationError, *_):
    """
    Представляет ошибку валидации данных в виде HTTP ответа.
    """
    raise format_http_error(HTTPBadRequest, 'Request validation has failed', error.messages)


@web.middleware
async def error_middleware(request: Request, handler):
    try:
        return await handler(request)
    except HTTPException as err:
        # Исключения которые представляют из себя HTTP ответ, были брошены
        # осознанно для отображения клиенту.

        # Текстовые исключения (или исключения без информации) форматируем
        # в JSON
        if not isinstance(err.body, JsonPayload):
            err = format_http_error(err.__class__, err.text)

        raise err

    except ValidationError as err:
        # Ошибки валидации, брошенные в обработчиках
        raise handle_validation_error(err)

    except Exception as exc:
        # Все остальные исключения не могут быть отображены клиенту в виде
        # HTTP ответа и могут случайно раскрыть внутреннюю информацию.
        log.exception('Unhandled exception')
        print(exc)
        raise format_http_error(HTTPInternalServerError)


@web.middleware
async def login_middleware(
    request: web.Request,
    handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.StreamResponse:
    """
    Проверяет, что пользователь аворизован и у него есть доступ к ресурсу
    """
    # user = await get_user(request)
    # if user is not None:
    #     request['USER'] = user
    # else:  # user is None
    #     if login_required(handler):
    #         raise web.HTTPSeeAlso(location='/login')

    # И прочий код проверки авторизации
    return await handler(request)
