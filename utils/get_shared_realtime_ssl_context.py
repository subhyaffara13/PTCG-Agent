from typing import Union

def get_shared_realtime_ssl_context() -> Union[bool, str, ssl.SSLContext]:
    """
    Lazily create the SSL context reused by realtime websocket clients so we avoid
    import-order cycles during startup while keeping a single shared configuration.
    """
    global _shared_realtime_ssl_context
    if _shared_realtime_ssl_context is None:
        _shared_realtime_ssl_context = get_ssl_configuration()
    return _shared_realtime_ssl_context

