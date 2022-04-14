from datetime import timedelta, datetime
from typing import Callable
from dataclasses import dataclass, field

import jwt
from aiohttp.web import Request, Response


ACCESS_TOKEN_SECRET = 'access-cool-secret-you-wont-hack-me'
REFRESH_TOKEN_SECRET = 'refresh-cool-secret-you-wont-hack-me'

ACCESS_TOKEN_TTL = timedelta(minutes=2).total_seconds()
REFRESH_TOKEN_TTL = timedelta(minutes=5).total_seconds()


@dataclass
class UserInfo:
    username: str = field()
    roles: set = field(default_factory=set)


def _is_expired(iat: float, ttl: float) -> int:
    print(f'{datetime.now().timestamp()} > {iat + ttl}')
    return datetime.now().timestamp() > iat + ttl


def authorized(func: Callable):
    def inner(request: Request):
        auth_scheme = 'Bearer '
        auth = request.headers.get('Authorization')

        if auth is None:
            return Response(body={'error': 'unauthorized user'}, status=401)

        if not auth.startswith(auth_scheme):
            return Response(body={'error': 'illegal auth scheme'}, status=401)

        try:
            user_info = jwt.decode(auth[len(auth_scheme):], ACCESS_TOKEN_SECRET, algorithms='HS256')
            print(user_info)
            if _is_expired(user_info['iat'], ACCESS_TOKEN_TTL):
                return Response(body={'error': 'access token is expired'}, status=401)

            username = user_info['username']
        except:  # noqa E722
            return Response(body={'error': 'wrong access token'}, status=401)

        return func(request, UserInfo(username, set()))
    return inner


def has_role(role):
    def decorator(func: Callable):
        def inner(*args, **kwargs):
            return func(args, kwargs)
        return inner
    return decorator
