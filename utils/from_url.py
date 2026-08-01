
def from_url(url: str, **kwargs: Any) -> "Redis":
    """
    Returns an active Redis client generated from the given database URL.

    Will attempt to extract the database id from the path url fragment, if
    none is provided.
    """
    from redis.client import Redis

    return Redis.from_url(url, **kwargs)


def from_url(url: str, **kwargs: Any) -> "Redis":
    """
    Returns an active Redis client generated from the given database URL.

    Will attempt to extract the database id from the path url fragment, if
    none is provided.
    """
    from redis.asyncio.client import Redis

    return Redis.from_url(url, **kwargs)

