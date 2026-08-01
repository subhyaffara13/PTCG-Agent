
def _init_async_redis_sentinel(redis_kwargs) -> async_redis.Redis:
    sentinel_nodes = redis_kwargs.get("sentinel_nodes")
    sentinel_password = redis_kwargs.get("sentinel_password")
    service_name = redis_kwargs.get("service_name")
    connection_kwargs = _get_redis_sentinel_connection_kwargs(redis_kwargs)
    connection_kwargs.setdefault("socket_timeout", REDIS_SOCKET_TIMEOUT)
    sentinel_kwargs = dict(connection_kwargs)
    sentinel_kwargs["password"] = sentinel_password

    if not sentinel_nodes or not service_name:
        raise ValueError(
            "Both 'sentinel_nodes' and 'service_name' are required for Redis Sentinel."
        )

    verbose_logger.debug("init_redis_sentinel: sentinel nodes are being initialized.")

    # Set up the Sentinel client
    sentinel = async_redis.Sentinel(
        sentinel_nodes,
        sentinel_kwargs=sentinel_kwargs,
    )

    # Return the master instance for the given service

    return sentinel.master_for(service_name, **connection_kwargs)

