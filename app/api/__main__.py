from aiohttp.web import run_app
from app.api.app import create_app


def main():
    app = create_app()
    run_app(app)


if __name__ == '__main__':
    main()
