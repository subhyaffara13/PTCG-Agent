
def is_connection_dropped(conn: BaseHTTPConnection) -> bool:  # Platform-specific
    """
    Returns True if the connection is dropped and should be closed.
    :param conn: :class:`urllib3.connection.HTTPConnection` object.
    """
    return not conn.is_connected


def is_connection_dropped(conn: BaseHTTPConnection) -> bool:  # Platform-specific
    """
    Returns True if the connection is dropped and should be closed.
    :param conn: :class:`urllib3.connection.HTTPConnection` object.
    """
    return not conn.is_connected

