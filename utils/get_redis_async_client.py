
def get_redis_async_client(
    connection_pool: Optional[async_redis.BlockingConnectionPool] = None,
    **env_overrides,
) -> Union[async_redis.Redis, async_redis.RedisCluster]:
    redis_kwargs = _get_redis_client_logic(**env_overrides)

    if "startup_nodes" in redis_kwargs:
        from redis.cluster import ClusterNode

        args = _get_redis_cluster_kwargs()
        cluster_kwargs = {}
        for arg in redis_kwargs:
            if arg in args:
                cluster_kwargs[arg] = redis_kwargs[arg]

        # Handle GCP IAM authentication for async clusters
        redis_connect_func = cluster_kwargs.pop("redis_connect_func", None)

        # Use a CredentialProvider so the IAM token is regenerated on every new
        # connection — mirrors the sync path where redis_connect_func is invoked
        # per connection.  Without this, the token would expire after ~1 hour.
        if redis_connect_func and hasattr(redis_connect_func, "_gcp_service_account"):
            cluster_kwargs["credential_provider"] = GCPIAMCredentialProvider(
                redis_connect_func._gcp_service_account
            )
        # Handle Azure AD authentication for async clusters via CredentialProvider
        # so the credential's internal cache + silent refresh runs per connection
        # (mirrors GCP IAM above; avoids static-token-baked-in-pool expiry).
        elif redis_connect_func and hasattr(redis_connect_func, "_azure_credential"):
            cluster_kwargs["credential_provider"] = AzureADCredentialProvider(
                redis_connect_func._azure_credential,
                username=os.environ.get("REDIS_USERNAME") or None,
            )

        new_startup_nodes: List[ClusterNode] = []

        for item in redis_kwargs["startup_nodes"]:
            new_startup_nodes.append(ClusterNode(**item))
        cluster_kwargs.pop("startup_nodes", None)

        # Create async RedisCluster with IAM token as password if available
        cluster_client = async_redis.RedisCluster(
            startup_nodes=new_startup_nodes, **cluster_kwargs  # type: ignore
        )

        return cluster_client

    if "url" in redis_kwargs and redis_kwargs["url"] is not None:
        if connection_pool is not None:
            return async_redis.Redis(connection_pool=connection_pool)
        args = _get_redis_url_kwargs(client=async_redis.Redis.from_url)
        url_kwargs = {}
        for arg in redis_kwargs:
            if arg in args:
                url_kwargs[arg] = redis_kwargs[arg]
            else:
                verbose_logger.debug(
                    "REDIS: ignoring argument: {}. Not an allowed async_redis.Redis.from_url arg.".format(
                        arg
                    )
                )
        return async_redis.Redis.from_url(**url_kwargs)

    # Check for Redis Sentinel
    if "sentinel_nodes" in redis_kwargs and "service_name" in redis_kwargs:
        return _init_async_redis_sentinel(redis_kwargs)

    # Wrap GCP / Azure AD auth in a CredentialProvider for the standard async
    # Redis client. The async client doesn't support redis_connect_func, but it
    # does honour credential_provider — which is called per connection, so the
    # underlying SDK can refresh tokens silently before they expire.
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

    _pretty_print_redis_config(redis_kwargs=redis_kwargs)

    if connection_pool is not None:
        redis_kwargs["connection_pool"] = connection_pool

    return async_redis.Redis(
        **redis_kwargs,
    )

