from aiohttp.web import Request, Response


async def ping(request: Request) -> Response:
    return Response(body={}, status=200)
