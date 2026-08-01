
def get_redis_client(**env_overrides):
    redis_kwargs = _get_redis_client_logic(**env_overrides)

    if "startup_nodes" in redis_kwargs:
        return init_redis_cluster(redis_kwargs)

    if "url" in redis_kwargs and redis_kwargs["url"] is not None:
        args = _get_redis_url_kwargs()
        url_kwargs = {}
        for arg in redis_kwargs:
            if arg in args:
                url_kwargs[arg] = redis_kwargs[arg]

        return redis.Redis.from_url(**url_kwargs)

    # Check for Redis Sentinel
    if "sentinel_nodes" in redis_kwargs and "service_name" in redis_kwargs:
        return _init_redis_sentinel(redis_kwargs)

    return redis.Redis(**redis_kwargs)

