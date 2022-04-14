from types import AsyncGeneratorType, MappingProxyType
from typing import AsyncIterable, Mapping

from aiohttp.web_app import Application
from aiohttp import PAYLOAD_REGISTRY
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware

from app.db.pg import setup_pg
from app.api.routes_configurator import setup_routes
from app.api.middlewares import error_middleware, handle_validation_error, login_middleware
from app.api.payloads import AsyncGenJSONListPayload, JsonPayload


def create_app() -> Application:
    app = Application(middlewares=[error_middleware, validation_middleware, login_middleware])
    setup_routes(app)

    # Добавил в список контекстный генератор обработки запуска/остановки приложения
    app.cleanup_ctx.append(setup_pg)

    # Создаёт Swagger-документацию для сервиса, которая доступна по адресу /api/docs
    setup_aiohttp_apispec(
        app=app,
        title="Документация simple-service",
        version="v0.0.1",
        url="/swagger.json",
        swagger_path="/",
        error_callback=handle_validation_error,
    )

    # Настройка сериализации в JSON
    PAYLOAD_REGISTRY.register(AsyncGenJSONListPayload, (AsyncGeneratorType, AsyncIterable))
    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))
    return app
