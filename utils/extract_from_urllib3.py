
def extract_from_urllib3() -> None:
    "Undo monkey-patching by :func:`inject_into_urllib3`."

    util.SSLContext = orig_util_SSLContext
    util.ssl_.SSLContext = orig_util_SSLContext
    util.IS_PYOPENSSL = False
    util.ssl_.IS_PYOPENSSL = False


def extract_from_urllib3() -> None:
    from .. import connection as urllib3_connection
    from .. import util as urllib3_util
    from ..connectionpool import HTTPSConnectionPool
    from ..util import ssl_ as urllib3_util_ssl

    HTTPSConnectionPool.ConnectionCls = orig_HTTPSConnection
    urllib3_connection.HTTPSConnection = orig_HTTPSConnection  # type: ignore[misc]

    urllib3_util.ALPN_PROTOCOLS = ["http/1.1"]
    urllib3_util_ssl.ALPN_PROTOCOLS = ["http/1.1"]


def extract_from_urllib3() -> None:
    "Undo monkey-patching by :func:`inject_into_urllib3`."

    util.SSLContext = orig_util_SSLContext
    util.ssl_.SSLContext = orig_util_SSLContext
    util.IS_PYOPENSSL = False
    util.ssl_.IS_PYOPENSSL = False


def extract_from_urllib3() -> None:
    from .. import connection as urllib3_connection
    from .. import util as urllib3_util
    from ..connectionpool import HTTPSConnectionPool
    from ..util import ssl_ as urllib3_util_ssl

    HTTPSConnectionPool.ConnectionCls = orig_HTTPSConnection
    urllib3_connection.HTTPSConnection = orig_HTTPSConnection  # type: ignore[misc]

    urllib3_util.ALPN_PROTOCOLS = ["http/1.1"]
    urllib3_util_ssl.ALPN_PROTOCOLS = ["http/1.1"]

