from marshmallow import Schema
from marshmallow.fields import (
    Int, Str, DateTime, List, Nested
)
from marshmallow.validate import Length, And, Email


class User(Schema):
    pass


# LANGUAGE

class Language(Schema):
    language_id = Int(required=True)
    name = Str(required=True, validate=Length(1, 31))


# COUNTRY

class Country(Schema):
    country_id = Int(required=True)
    name = Str(required=True, validate=Length(1, 31))


# GROUP

class Group(Schema):
    group_id = Int(required=True)
    name = Str(required=True, validate=Length(1, 31))
    participants_count = Int(required=True)


class GroupDetail(Schema):
    group_id = Int(required=True)
    name = Str(required=True, validate=Length(1, 31))
    owner = Nested(User, required=True)
    participants = List(Nested(User), required=True)


# USER

class User(Schema):
    user_id = Int(required=True)
    first_name = Str(required=True, validate=Length(1, 31))
    last_name = Str(required=True, validate=Length(1, 31))


class UserDetail(Schema):
    user_id = Int(required=True)
    first_name = Str(required=True, validate=Length(1, 31))
    last_name = Str(required=True, validate=Length(1, 31))
    birth_date = DateTime()
    country = Str(validate=Length(1, 31))

    friends = List(Nested(User), required=True)
    groups = List(Nested(Group), required=True)


class CreateUser(Schema):
    email = Str(required=True, validate=And(Email(), Length(3, 31)))
    password = Str(required=True, validate=Length(3, 31))

    first_name = Str(required=True, validate=Length(1, 31))
    last_name = Str(required=True, validate=Length(1, 31))
    birth_date = DateTime()
    country = Int()


# POST

class CreatePost(Schema):
    """Схема запроса на создания поста"""
    user_id = Int(required=True)
    post_text = Str(required=True, validate=Length(1, 255))


class Post(Schema):
    """Схема поста ответа"""
    user = Nested(User, required=True)
    time = DateTime(required=True)
    post_text = Str(required=True, validate=Length(1, 255))


class UsersPosts(Schema):
    """Посты (записи на стене пользователя) - ответ"""
    user_id = Int(required=True)
    posts = List(Nested(Post), required=True)


class NewsForUser(Schema):
    """"Лента новостей (постов) для пользователя - ответ"""
    for_user_id = Int(required=True)
    news = List(Nested(Post), required=True)


# AUTH

class AuthRequest(Schema):
    login = Str(required=True)
    password = Str(required=True)


class AuthResponse(Schema):
    access_token = Str(required=True)
    refresh_token = Str(required=True)
    token_type = Str(required=True)
    expires_in = Int(required=True)
    refresh_expires_in = Int(required=True)

    username = Str(required=True)
    # roles = List(required=True)


class RefreshRequest(Schema):
    username = Str(required=True)
    refresh_token = Str(required=True)
