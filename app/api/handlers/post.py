from aiohttp.web import Request, Response
from aiohttp_apispec import request_schema
from marshmallow import ValidationError

from app.api.schema import PostCreateSchema


@request_schema(PostCreateSchema)
async def create_post(request: Request) -> Response:
    body = await request.json()
    print(body)

    schema = PostCreateSchema()
    try:
        pass
        # result = schema.load(body)
    except ValidationError as err:
        return Response(text=str(err.messages), status=400)

    return Response(text=schema.dumps(schema.load(body)), status=200)


def get_news(user_id: int) -> list:
    """Get news feed (posts) for user by id"""
    pass


def get_user_posts(user_id: int) -> list:
    """Get user's posts by id (posts which he published)"""
    pass
