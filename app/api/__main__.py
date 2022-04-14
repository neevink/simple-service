import logging
from aiomisc.log import basic_config

from aiohttp.web import run_app
from app.api.app import create_app


def main():
    # запускаем логирование в отдельном потоке, потому что приложение фсинхронное
    basic_config(logging.DEBUG, buffered=True)

    app = create_app()
    run_app(app)


if __name__ == '__main__':
    main()
