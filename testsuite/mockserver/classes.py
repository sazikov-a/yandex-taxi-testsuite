import dataclasses
import pathlib
import typing

import aiohttp.web

from testsuite import annotations
from testsuite.utils import callinfo, http, url_util

GenericRequestHandler = typing.Callable[
    ...,
    annotations.MaybeAsyncResult[aiohttp.web.Response],
]
GenericRequestDecorator = typing.Callable[
    [GenericRequestHandler],
    callinfo.AsyncCallQueue,
]
JsonRequestHandler = typing.Callable[
    ...,
    annotations.MaybeAsyncResult[
        typing.Union[aiohttp.web.Response, annotations.JsonAnyOptional]
    ],
]
JsonRequestDecorator = typing.Callable[
    [JsonRequestHandler],
    callinfo.AsyncCallQueue,
]
MockserverRequest = http.Request


@dataclasses.dataclass(frozen=True)
class SslCertInfo:
    cert_path: str
    private_key_path: str


@dataclasses.dataclass(frozen=True)
class MockserverInfo:
    host: typing.Optional[str]
    port: typing.Optional[int]
    base_url: str
    ssl: typing.Optional[SslCertInfo]
    socket_path: typing.Optional[pathlib.Path] = None

    def url(self, path: str) -> str:
        """Concats ``base_url`` and provided ``path``."""
        return url_util.join(self.base_url, path)

    def get_host_header(self) -> str:
        if self.socket_path:
            return str(self.socket_path)

        if not self.host and not self.port:
            raise RuntimeError(
                'either host and port or socket_path must be set in mockserver info'
            )

        if self.port == 80:
            return str(self.host)
        return f'{self.host}:{self.port}'


class MockserverSslInfo(MockserverInfo):
    ssl: SslCertInfo


MockserverInfoFixture = MockserverInfo
MockserverSslInfoFixture = typing.Optional[MockserverInfo]
