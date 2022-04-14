from aiohttp.web import Application
from asyncpgsa import PG
from sqlalchemy import create_engine

from app.db.schema import metadata

DEFAULT_URL = 'postgresql://kirill:1@localhost/test_db'
MAX_QUERY_ARGS = 32767
MAX_INTEGER = 2147483647

pg_pool_min_size = 3
pg_pool_max_size = 10


async def setup_pg(app: Application) -> PG:
    app['db'] = PG()
    await app['db'].init(  # Create connection pool
        DEFAULT_URL,
        min_size=pg_pool_min_size,
        max_size=pg_pool_max_size,
    )

    await app['db'].fetchval('SELECT 1')
    print('Connected to database')
    # log.info('Connected to database %s', DEFAULT_URL)

    print('Creating database tables')
    await _create_tables()
    print('Database tables is created')

    try:
        yield
    finally:
        print('Disconnecting from database')
        # log.info('Disconnecting from database %s', db_info)
        await app['db'].pool.close()
        print('Disconnected from database')
        # log.info('Disconnected from database %s', db_info)


async def _create_tables():
    engine = create_engine(DEFAULT_URL, echo=True)
    metadata.create_all(engine)
