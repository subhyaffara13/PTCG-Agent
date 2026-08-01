
def inject_into_urllib3() -> None:
    "Monkey-patch urllib3 with PyOpenSSL-backed SSL-support."

    _validate_dependencies_met()

    util.SSLContext = PyOpenSSLContext  # type: ignore[assignment]
    util.ssl_.SSLContext = PyOpenSSLContext  # type: ignore[assignment]
    util.IS_PYOPENSSL = True
    util.ssl_.IS_PYOPENSSL = True


def inject_into_urllib3() -> None:
    # First check if h2 version is valid
    h2_version = version("h2")
    if not h2_version.startswith("4."):
        raise ImportError(
            "urllib3 v2 supports h2 version 4.x.x, currently "
            f"the 'h2' module is compiled with {h2_version!r}. "
            "See: https://github.com/urllib3/urllib3/issues/3290"
        )

    # Import here to avoid circular dependencies.
    from .. import connection as urllib3_connection
    from .. import util as urllib3_util
    from ..connectionpool import HTTPSConnectionPool
    from ..util import ssl_ as urllib3_util_ssl
    from .connection import HTTP2Connection

    global orig_HTTPSConnection
    orig_HTTPSConnection = urllib3_connection.HTTPSConnection

    HTTPSConnectionPool.ConnectionCls = HTTP2Connection
    urllib3_connection.HTTPSConnection = HTTP2Connection  # type: ignore[misc]

    # TODO: Offer 'http/1.1' as well, but for testing purposes this is handy.
    urllib3_util.ALPN_PROTOCOLS = ["h2"]
    urllib3_util_ssl.ALPN_PROTOCOLS = ["h2"]


def inject_into_urllib3() -> None:
    # override connection classes to use emscripten specific classes
    # n.b. mypy complains about the overriding of classes below
    # if it isn't ignored
    HTTPConnectionPool.ConnectionCls = EmscriptenHTTPConnection
    HTTPSConnectionPool.ConnectionCls = EmscriptenHTTPSConnection
    urllib3.connection.HTTPConnection = EmscriptenHTTPConnection  # type: ignore[misc,assignment]
    urllib3.connection.HTTPSConnection = EmscriptenHTTPSConnection  # type: ignore[misc,assignment]
    urllib3.connection.VerifiedHTTPSConnection = EmscriptenHTTPSConnection  # type: ignore[assignment]


def inject_into_urllib3() -> None:
    "Monkey-patch urllib3 with PyOpenSSL-backed SSL-support."

    _validate_dependencies_met()

    util.SSLContext = PyOpenSSLContext  # type: ignore[assignment]
    util.ssl_.SSLContext = PyOpenSSLContext  # type: ignore[assignment]
    util.IS_PYOPENSSL = True
    util.ssl_.IS_PYOPENSSL = True


def inject_into_urllib3() -> None:
    # First check if h2 version is valid
    h2_version = version("h2")
    if not h2_version.startswith("4."):
        raise ImportError(
            "urllib3 v2 supports h2 version 4.x.x, currently "
            f"the 'h2' module is compiled with {h2_version!r}. "
            "See: https://github.com/urllib3/urllib3/issues/3290"
        )

    # Import here to avoid circular dependencies.
    from .. import connection as urllib3_connection
    from .. import util as urllib3_util
    from ..connectionpool import HTTPSConnectionPool
    from ..util import ssl_ as urllib3_util_ssl
    from .connection import HTTP2Connection

    global orig_HTTPSConnection
    orig_HTTPSConnection = urllib3_connection.HTTPSConnection

    HTTPSConnectionPool.ConnectionCls = HTTP2Connection
    urllib3_connection.HTTPSConnection = HTTP2Connection  # type: ignore[misc]

    # TODO: Offer 'http/1.1' as well, but for testing purposes this is handy.
    urllib3_util.ALPN_PROTOCOLS = ["h2"]
    urllib3_util_ssl.ALPN_PROTOCOLS = ["h2"]


def inject_into_urllib3() -> None:
    # override connection classes to use emscripten specific classes
    # n.b. mypy complains about the overriding of classes below
    # if it isn't ignored
    HTTPConnectionPool.ConnectionCls = EmscriptenHTTPConnection
    HTTPSConnectionPool.ConnectionCls = EmscriptenHTTPSConnection
    urllib3_connection.HTTPConnection = EmscriptenHTTPConnection  # type: ignore[misc,assignment]
    urllib3_connection.HTTPSConnection = EmscriptenHTTPSConnection  # type: ignore[misc,assignment]
    urllib3_connection.VerifiedHTTPSConnection = EmscriptenHTTPSConnection  # type: ignore[assignment]

