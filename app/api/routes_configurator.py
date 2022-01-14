from aiohttp import web

from app.api.handlers.ping import ping
from app.api.handlers.post import get_user_posts, get_news, create_post
from app.api.handlers.profile import get_profile


def setup_routes(app: web.Application) -> None:
    app.add_routes(
        [
            web.get('/ping', ping),

            web.get('/profile', get_profile),
            web.get('/posts', get_user_posts),
            web.get('/news', get_news),

            web.post('/post', create_post),
        ]
    )
