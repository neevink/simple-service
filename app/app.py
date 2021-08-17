from aiohttp import web
from aiohttp.web import Request, Response
from marshmallow import ValidationError

from schema import CustomerSchema

from aiohttp_apispec import response_schema, request_schema, setup_aiohttp_apispec


async def handle(request):
    return web.Response(text='It works')


@request_schema(CustomerSchema)
async def post_customer(request: Request) -> Response:
    body = await request.json()
    print(body)

    schema = CustomerSchema()
    try:
        result = schema.load(body)
    except ValidationError as err:
        return Response(text=str(err.messages), status=400)

    return Response(text=schema.dumps(schema.load(body)), status=200)


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes(
        [
            web.get('/', handle),
            web.post('/customer', post_customer)
        ]
    )

    # Создаёт Swagger-документацию для сервиса, которая доступна по адресу /api/docs
    setup_aiohttp_apispec(
        app=app,
        title="Документация simple-service",
        version="v1",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs",
    )

    return app


if __name__ == '__main__':
    web.run_app(create_app())
