import asyncio
import pathlib
import socket
import contextlib

DEFAULT_BACKLOG = 50


@contextlib.asynccontextmanager
async def _create_server(factory, *, loop=None, **kwargs):
    if loop is None:
        loop = _get_running_loop()
    server = await loop.create_server(factory, **kwargs)
    try:
        yield server
    finally:
        server.close()
        await server.wait_closed()


def create_tcp_server(
    factory,
    *,
    loop=None,
    host='localhost',
    port=0,
    sock=None,
    **kwargs,
):
    if sock is None:
        sock = bind_socket(host, port)
    return _create_server(factory, loop=loop, sock=sock, **kwargs)


def bind_socket(
    hostname='localhost',
    port=0,
    family=socket.AF_INET,
    backlog=DEFAULT_BACKLOG,
):
    sock = socket.socket(family)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((hostname, port))
    sock.listen(backlog)
    return sock


@contextlib.asynccontextmanager
async def _create_unix_server(factory, *, loop=None, **kwargs):
    if loop is None:
        loop = _get_running_loop()
    server = await loop.create_unix_server(factory, **kwargs)
    try:
        yield server
    finally:
        server.close()
        await server.wait_closed()


def create_unix_server(
    factory,
    path: pathlib.Path,
    *,
    loop=None,
    sock=None,
    **kwargs,
):
    return _create_unix_server(
        factory, loop=loop, path=path, sock=sock, **kwargs
    )


if hasattr(asyncio, 'get_running_loop'):
    _get_running_loop = asyncio.get_running_loop
else:
    _get_running_loop = asyncio.get_event_loop
