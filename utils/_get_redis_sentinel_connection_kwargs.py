
def _get_redis_sentinel_connection_kwargs(redis_kwargs: dict) -> dict:
    connection_kwargs = {}
    args = _get_redis_kwargs()
    for arg in redis_kwargs:
        if arg in args:
            connection_kwargs[arg] = redis_kwargs[arg]

    return connection_kwargs

