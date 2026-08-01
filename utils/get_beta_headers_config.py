
def get_beta_headers_config(url: str) -> dict:
    """
    Public entry point — returns the beta headers config dict.

    1. If ``LITELLM_LOCAL_ANTHROPIC_BETA_HEADERS`` is set, uses the local backup only.
    2. Otherwise fetches from ``url``, validates integrity, and falls back
       to the local backup on any failure.

    Args:
        url: URL to fetch the remote beta headers configuration from

    Returns:
        Dict containing the beta headers configuration
    """
    # Check if local-only mode is enabled
    if os.getenv("LITELLM_LOCAL_ANTHROPIC_BETA_HEADERS", "").lower() == "true":
        # verbose_logger.debug("Using local Anthropic beta headers config (LITELLM_LOCAL_ANTHROPIC_BETA_HEADERS=True)")
        return GetAnthropicBetaHeadersConfig.load_local_beta_headers_config()

    try:
        content = GetAnthropicBetaHeadersConfig.fetch_remote_beta_headers_config(url)
    except Exception as e:
        verbose_logger.warning(
            "LiteLLM: Failed to fetch remote beta headers config from %s: %s. "
            "Falling back to local backup.",
            url,
            str(e),
        )
        return GetAnthropicBetaHeadersConfig.load_local_beta_headers_config()

    # Validate the fetched config
    if not GetAnthropicBetaHeadersConfig.validate_beta_headers_config(
        fetched_config=content
    ):
        verbose_logger.warning(
            "LiteLLM: Fetched beta headers config failed integrity check. "
            "Using local backup instead. url=%s",
            url,
        )
        return GetAnthropicBetaHeadersConfig.load_local_beta_headers_config()

    return content

