
def _get_redis_cluster_kwargs(client=None):
    if client is None:
        client = redis.Redis.from_url
    arg_spec = inspect.getfullargspec(redis.RedisCluster)

    # Only allow primitive arguments
    exclude_args = {"self", "connection_pool", "retry", "host", "port", "startup_nodes"}

    available_args = {x for x in arg_spec.args if x not in exclude_args}
    available_args |= {
        "password",
        "username",
        "ssl",
        "ssl_cert_reqs",
        "ssl_check_hostname",
        "ssl_ca_certs",
        "redis_connect_func",  # Needed for sync clusters and IAM detection
        "gcp_service_account",
        "gcp_ssl_ca_certs",
        "azure_redis_ad_token",
        "azure_client_id",
        "azure_tenant_id",
        "azure_client_secret",
        "max_connections",
        "socket_timeout",
        "socket_connect_timeout",
    }

    return available_args

