from datetime import datetime

import jwt
from aiohttp.web import Request, Response
from aiohttp_apispec import request_schema, response_schema, docs

from app.api.schema import AuthRequest, AuthResponse, RefreshRequest
from app.api.authorization import (
    ACCESS_TOKEN_SECRET, REFRESH_TOKEN_SECRET, ACCESS_TOKEN_TTL, REFRESH_TOKEN_TTL
)


users_database = {
    'kirill': '1',
    'admin': '1',
}


def _expires_date(ttl: float) -> int:
    return round(datetime.now().timestamp() + ttl)


@docs(
    summary='Receive access and refresh tokens',
)
@request_schema(AuthRequest)
@response_schema(AuthResponse)
async def login(request: Request) -> Response:
    body = await request.json()

    login = body['login']
    password = body['password']

    if users_database.get(login) != password:
        return Response(body={'error': 'wrong login or password'}, status=400)

    issued_at = round(datetime.now().timestamp())

    payload = {
        'username': login,
        'iat': issued_at,
    }

    access_token = jwt.encode(payload, ACCESS_TOKEN_SECRET, algorithm='HS256')
    refresh_token = jwt.encode(payload, REFRESH_TOKEN_SECRET, algorithm='HS256')

    return Response(
        body={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': _expires_date(ACCESS_TOKEN_TTL),
            'refresh_expires_in': _expires_date(REFRESH_TOKEN_TTL),

            'username': login,
            'roles': [],
        },
        status=200,
    )


@docs(
    summary='Refresh (update) access and refresh tokens'
)
@request_schema(RefreshRequest)
@response_schema(AuthResponse)
async def refresh(request: Request) -> Response:
    body = await request.json()

    try:
        user_info = jwt.decode(body['refresh_token'], REFRESH_TOKEN_SECRET, algorithms='HS256')

        if user_info['iat'] + REFRESH_TOKEN_TTL < datetime.now().timestamp():
            return Response(body={'error': 'refresh token is expired'}, status=401)

        if user_info['username'] != body['username']:
            return Response(body={'error': 'wrong refresh token'}, status=401)

        issued_at = round(datetime.now().timestamp())
        new_payload = {
            'username': user_info['username'],
            'iat': issued_at,
        }

        access_token = jwt.encode(new_payload, ACCESS_TOKEN_SECRET, algorithm='HS256')
        refresh_token = jwt.encode(new_payload, REFRESH_TOKEN_SECRET, algorithm='HS256')

        return Response(
            body={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': _expires_date(ACCESS_TOKEN_TTL),
                'refresh_expires_in': _expires_date(REFRESH_TOKEN_TTL),

                'username': new_payload['username'],
                'roles': [],
            },
            status=200,
        )
    except:  # noqa E722
        return Response(body={'error': 'wrong refresh token'}, status=401)
