from aiohttp.web import Request, Response
from aiohttp_apispec import docs, response_schema

from app.api.schema import UserDetail


@docs(
    summary="Get user profile by id",
)
@response_schema(UserDetail)
def get_profile(request: Request):
    user_id = int(request.match_info.get('user_id'))
    return Response(body={'user_id': user_id}, status=200)
