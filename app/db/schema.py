from enum import unique, Enum

from sqlalchemy import (
    Column, Date, Enum as PgEnum, ForeignKey, ForeignKeyConstraint, Integer,
    String, Table,
)

from app.db.conventions import metadata


@unique
class Gender(Enum):
    female = 'female'
    male = 'male'


# LANGUAGE

languages_table = Table(
    'languages',
    metadata,
    Column('language_id', Integer, primary_key=True),
    Column('name', String, primary_key=True),
)


# COUNTRY

countries_table = Table(
    'countries',
    metadata,
    Column('country_id', Integer, primary_key=True),
    Column('name', String, nullable=False),
)


# GROUP

groups_table = Table(
    'groups',
    metadata,
    Column('group_id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('owner', Integer, ForeignKey('users.user_id')),
)

users_groups_table = Table(
    'users_groups',
    metadata,
    Column('group_id', Integer),
    Column('user_id', Integer),
#    ForeignKeyConstraint(
#        ('group_id', 'user_id'),
#        ('groups.group_id', 'users.user_id'),
#    ),
)


# USER

users_table = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('birth_date', Date, nullable=False),
    Column('country_id', Integer, ForeignKey('countries.country_id')),
    Column('gender', PgEnum(Gender, name='gender'), nullable=False),  # TODO: Add enum to marshmallow schema
)

friends_table = Table(
    'friends',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('friend_id', Integer, primary_key=True),
    #ForeignKeyConstraint(
    #    ('user_id', 'friend_id'),
    #    ('users.user_id', 'users.user_id'),
    #),
)

