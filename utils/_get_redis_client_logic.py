
def _get_redis_client_logic(**env_overrides):
    """
    Common functionality across sync + async redis client implementations
    """
    ### check if "os.environ/<key-name>" passed in
    for k, v in env_overrides.items():
        if isinstance(v, str) and v.startswith("os.environ/"):
            v = v.replace("os.environ/", "")
            value = get_secret(v)  # type: ignore
            env_overrides[k] = value

    redis_kwargs = {
        **_redis_kwargs_from_environment(),
        **env_overrides,
    }

    _startup_nodes: Optional[Union[str, list]] = redis_kwargs.get("startup_nodes", None) or get_secret(  # type: ignore
        "REDIS_CLUSTER_NODES"
    )

    # If startup_nodes resolved to None (not set by kwarg or env), remove the key
    # entirely so callers can rely on key presence as a reliable cluster-mode signal.
    if _startup_nodes is not None and isinstance(_startup_nodes, str):
        redis_kwargs["startup_nodes"] = json.loads(_startup_nodes)
    elif _startup_nodes is None:
        redis_kwargs.pop("startup_nodes", None)

    _sentinel_nodes: Optional[Union[str, list]] = redis_kwargs.get("sentinel_nodes", None) or get_secret(  # type: ignore
        "REDIS_SENTINEL_NODES"
    )

    if _sentinel_nodes is not None and isinstance(_sentinel_nodes, str):
        redis_kwargs["sentinel_nodes"] = json.loads(_sentinel_nodes)

    _sentinel_password: Optional[str] = redis_kwargs.get(
        "sentinel_password", None
    ) or get_secret_str("REDIS_SENTINEL_PASSWORD")

    if _sentinel_password is not None:
        redis_kwargs["sentinel_password"] = _sentinel_password

    _service_name: Optional[str] = redis_kwargs.get("service_name", None) or get_secret(  # type: ignore
        "REDIS_SERVICE_NAME"
    )

    if _service_name is not None:
        redis_kwargs["service_name"] = _service_name

    # Handle GCP IAM authentication
    _gcp_service_account = redis_kwargs.get("gcp_service_account") or get_secret_str(
        "REDIS_GCP_SERVICE_ACCOUNT"
    )
    _gcp_ssl_ca_certs = redis_kwargs.get("gcp_ssl_ca_certs") or get_secret_str(
        "REDIS_GCP_SSL_CA_CERTS"
    )

    if _gcp_service_account is not None:
        verbose_logger.debug(
            "Setting up GCP IAM authentication for Redis with service account."
        )
        redis_kwargs["redis_connect_func"] = create_gcp_iam_redis_connect_func(
            service_account=_gcp_service_account, ssl_ca_certs=_gcp_ssl_ca_certs
        )
        # Store GCP service account in redis_connect_func for async cluster access
        redis_kwargs["redis_connect_func"]._gcp_service_account = _gcp_service_account  # type: ignore[attr-defined]

        # Remove GCP-specific kwargs that shouldn't be passed to Redis client
        redis_kwargs.pop("gcp_service_account", None)
        redis_kwargs.pop("gcp_ssl_ca_certs", None)

        # Only enable SSL if explicitly requested AND SSL CA certs are provided
        if _gcp_ssl_ca_certs and redis_kwargs.get("ssl", False):
            redis_kwargs["ssl_ca_certs"] = _gcp_ssl_ca_certs

    # Handle Azure AD authentication (after GCP IAM block)
    _azure_redis_ad_token = redis_kwargs.get("azure_redis_ad_token") or get_secret(
        "REDIS_AZURE_AD_TOKEN"
    )

    _azure_ad_enabled = (
        _azure_redis_ad_token is not None
        and str(_azure_redis_ad_token).lower() == "true"
    )

    if _azure_ad_enabled and _gcp_service_account is not None:
        verbose_logger.warning(
            "Both GCP IAM (gcp_service_account) and Azure AD (azure_redis_ad_token) are configured for Redis. "
            "Using GCP IAM. Remove one to avoid misconfiguration."
        )

    if _azure_ad_enabled and _gcp_service_account is None:
        _azure_client_id = redis_kwargs.get("azure_client_id") or get_secret_str(
            "AZURE_CLIENT_ID"
        )
        _azure_tenant_id = redis_kwargs.get("azure_tenant_id") or get_secret_str(
            "AZURE_TENANT_ID"
        )
        _azure_client_secret = redis_kwargs.get(
            "azure_client_secret"
        ) or get_secret_str("AZURE_CLIENT_SECRET")

        verbose_logger.debug("Setting up Azure AD authentication for Redis.")
        redis_kwargs["redis_connect_func"] = create_azure_ad_redis_connect_func(
            azure_client_id=_azure_client_id,
            azure_tenant_id=_azure_tenant_id,
            azure_client_secret=_azure_client_secret,
        )
        # Marker for async paths to detect Azure AD auth. The live credential
        # object is attached separately as `_azure_credential` by
        # `create_azure_ad_redis_connect_func`; the raw client_id/tenant_id/secret
        # are intentionally NOT exposed on the function to avoid leaking
        # credentials via inspection or logging.
        redis_kwargs["redis_connect_func"]._azure_redis_ad_token = True  # type: ignore[attr-defined]

    # Always remove Azure-specific kwargs that shouldn't be passed to Redis client
    redis_kwargs.pop("azure_redis_ad_token", None)
    redis_kwargs.pop("azure_client_id", None)
    redis_kwargs.pop("azure_tenant_id", None)
    redis_kwargs.pop("azure_client_secret", None)

    if "url" in redis_kwargs and redis_kwargs["url"] is not None:
        # Only strip host/port/db/password when not routing to a cluster.
        # When startup_nodes is also present the cluster path takes priority and
        # needs the password for authentication.
        if not redis_kwargs.get("startup_nodes"):
            redis_kwargs.pop("host", None)
            redis_kwargs.pop("port", None)
            redis_kwargs.pop("db", None)
            redis_kwargs.pop("password", None)
    elif "startup_nodes" in redis_kwargs and redis_kwargs["startup_nodes"] is not None:
        pass
    elif (
        "sentinel_nodes" in redis_kwargs and redis_kwargs["sentinel_nodes"] is not None
    ):
        pass
    elif "host" not in redis_kwargs or redis_kwargs["host"] is None:
        raise ValueError("Either 'host' or 'url' must be specified for redis.")

    # litellm.print_verbose(f"redis_kwargs: {redis_kwargs}")
    return redis_kwargs

