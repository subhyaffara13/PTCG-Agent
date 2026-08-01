
def get_weave_otel_config() -> WeaveOtelConfig:
    """
    Retrieves the Weave OpenTelemetry configuration based on environment variables.

    Environment Variables:
        WANDB_API_KEY: Required. W&B API key for authentication.
        WANDB_PROJECT_ID: Required. Project ID in format <entity>/<project_name>.
        WANDB_HOST: Optional. Custom Weave host URL. Defaults to cloud endpoint.

    Returns:
        WeaveOtelConfig: A Pydantic model containing Weave OTEL configuration.

    Raises:
        ValueError: If required environment variables are missing.
    """
    api_key = os.getenv("WANDB_API_KEY")
    project_id = os.getenv("WANDB_PROJECT_ID")
    host = os.getenv("WANDB_HOST")

    if not api_key:
        raise ValueError(
            "WANDB_API_KEY must be set for Weave OpenTelemetry integration."
        )

    if not project_id:
        raise ValueError(
            "WANDB_PROJECT_ID must be set for Weave OpenTelemetry integration. Format: <entity>/<project_name>"
        )

    if host:
        if not host.startswith("http"):
            host = "https://" + host
        # Self-managed instances use a different path
        endpoint = host.rstrip("/") + WEAVE_OTEL_ENDPOINT
        verbose_logger.debug(f"Using Weave OTEL endpoint from host: {endpoint}")
    else:
        endpoint = WEAVE_BASE_URL + WEAVE_OTEL_ENDPOINT
        verbose_logger.debug(f"Using Weave cloud endpoint: {endpoint}")

    # Weave uses Basic auth with format: api:<WANDB_API_KEY>
    auth_header = _get_weave_authorization_header(api_key=api_key)
    otlp_auth_headers = f"Authorization={auth_header},project_id={project_id}"

    # Set standard OTEL environment variables
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = endpoint
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = otlp_auth_headers

    return WeaveOtelConfig(
        otlp_auth_headers=otlp_auth_headers,
        endpoint=endpoint,
        project_id=project_id,
        protocol="otlp_http",
    )

