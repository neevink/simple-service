from aiohttp import web

from aiohttp_apispec import setup_aiohttp_apispec

from app.api.routes_configurator import setup_routes


def create_app() -> web.Application:
    app = web.Application()
    setup_routes(app)

    # Создаёт Swagger-документацию для сервиса, которая доступна по адресу /api/docs
    setup_aiohttp_apispec(
        app=app,
        title="Документация simple-service",
        version="v1",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs",
    )

    return app
