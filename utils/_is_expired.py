import time

def _is_expired(connection_info: XetConnectionInfo) -> bool:
    """Check if the given XET connection info is expired."""
    return connection_info.expiration_unix_epoch <= int(time.time()) + XET_CONNECTION_INFO_SAFETY_PERIOD

