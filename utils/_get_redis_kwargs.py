
def _get_redis_kwargs():
    arg_spec = inspect.getfullargspec(redis.Redis)

    # Only allow primitive arguments
    exclude_args = {
        "self",
        "connection_pool",
        "retry",
    }

    include_args = {
        "url",
        "redis_connect_func",
        "gcp_service_account",
        "gcp_ssl_ca_certs",
        "azure_redis_ad_token",
        "azure_client_id",
        "azure_tenant_id",
        "azure_client_secret",
    }

    available_args = {x for x in arg_spec.args if x not in exclude_args} | include_args

    return available_args

