from aiohttp import web

from app.api.handlers.ping import ping
from app.api.handlers.post import get_user_posts, get_news, create_post
from app.api.handlers.profile import get_profile
from app.api.handlers.user import create_user


def setup_routes(app: web.Application) -> None:
    app.add_routes(
        [
            web.get(r'/ping', ping),

            web.post(r'/user', create_user),

            web.get(r'/profile/{user_id:\d+}', get_profile),

            web.get(r'/posts/{user_id:\d+}', get_user_posts),
            web.post(r'/post', create_post),
            web.get(r'/news/{for_user_id:\d+}', get_news),
        ]
    )
