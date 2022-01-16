from aiohttp.web import Request, Response
from aiohttp_apispec import request_schema, response_schema, docs

from app.api.schema import CreatePost, UsersPosts, NewsForUser, Post


@docs(
    summary="Create a new post",
)
@request_schema(CreatePost)
@response_schema(Post)
async def create_post(request: Request) -> Response:
    return Response(body={}, status=200)


@docs(
    summary="Get posts from users' page",
)
@response_schema(UsersPosts)
def get_user_posts(request: Request) -> list:
    user_id = int(request.match_info.get('user_id'))
    return Response(body={'user_id': user_id}, status=200)


@docs(
    summary="Get news feed for user by id",
)
@response_schema(NewsForUser)
def get_news(request: Request) -> list:
    for_user_id = int(request.match_info.get('for_user_id'))
    return Response(body={'user_id': for_user_id}, status=200)
