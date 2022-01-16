from aiohttp.web import Request, Response
from aiohttp_apispec import docs, request_schema, response_schema

from app.api.schema import CreateUser, UserDetail


@docs(
    summary="Create a new user account",
)
@request_schema(CreateUser)
@response_schema(UserDetail)
def create_user(request: Request):
    return Response(body={}, status=200)
