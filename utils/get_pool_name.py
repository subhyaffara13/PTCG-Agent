
def get_pool_name(pool: Union["ConnectionPoolInterface", "ConnectionPool"]) -> str:
    """
    Get a short string representation of a connection pool for observability.

    This provides a concise pool identifier suitable for use as a metric attribute,
    in the format: host:port_uniqueID (matching go-redis format)

    Args:
        pool: Connection pool instance

    Returns:
        Short pool name in format "host:port_uniqueID"

    Example:
        >>> pool = ConnectionPool(host='localhost', port=6379, db=0)
        >>> get_pool_name(pool)
        'localhost:6379_a1b2c3d4'
    """
    host = pool.connection_kwargs.get("host", "unknown")
    port = pool.connection_kwargs.get("port", 6379)

    # Get unique pool ID if available (added for observability)
    pool_id = getattr(pool, "_pool_id", "")

    if pool_id:
        return f"{host}:{port}_{pool_id}"
    else:
        return f"{host}:{port}"

