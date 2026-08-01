
def get_redis_connection_pool(
    **env_overrides,
) -> Optional[async_redis.BlockingConnectionPool]:
    redis_kwargs = _get_redis_client_logic(**env_overrides)
    verbose_logger.debug("get_redis_connection_pool: redis_kwargs", redis_kwargs)

    if "startup_nodes" in redis_kwargs:
        return None

    if "url" in redis_kwargs and redis_kwargs["url"] is not None:
        pool_kwargs = {
            "timeout": REDIS_CONNECTION_POOL_TIMEOUT,
            "url": redis_kwargs["url"],
        }
        if "max_connections" in redis_kwargs:
            try:
                pool_kwargs["max_connections"] = int(redis_kwargs["max_connections"])
            except (TypeError, ValueError):
                verbose_logger.warning(
                    "REDIS: invalid max_connections value %r, ignoring",
                    redis_kwargs["max_connections"],
                )
        return async_redis.BlockingConnectionPool.from_url(**pool_kwargs)

    # Wrap GCP / Azure AD auth in a CredentialProvider so pool-managed
    # connections re-fetch tokens via the SDK's internal cache + silent refresh
    # rather than reusing a single token captured at pool creation.
    redis_connect_func = redis_kwargs.pop("redis_connect_func", None)
    if redis_connect_func and hasattr(redis_connect_func, "_azure_credential"):
        redis_kwargs["credential_provider"] = AzureADCredentialProvider(
            redis_connect_func._azure_credential,
            username=os.environ.get("REDIS_USERNAME") or None,
        )
    elif redis_connect_func and hasattr(redis_connect_func, "_gcp_service_account"):
        redis_kwargs["credential_provider"] = GCPIAMCredentialProvider(
            redis_connect_func._gcp_service_account
        )

    connection_class = async_redis.Connection
    if "ssl" in redis_kwargs:
        connection_class = async_redis.SSLConnection
        redis_kwargs.pop("ssl", None)
        redis_kwargs["connection_class"] = connection_class
    return async_redis.BlockingConnectionPool(
        timeout=REDIS_CONNECTION_POOL_TIMEOUT, **redis_kwargs
    )

