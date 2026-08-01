
def sanitize_openai_provider_metadata(
    metadata: Optional[Dict[str, Any]],
) -> Optional[Dict[str, str]]:
    """
    Keep only provider-safe OpenAI metadata entries (string keys -> string values).

    Strips LiteLLM proxy-internal tracking fields that must not be forwarded to
    OpenAI batch/file APIs.
    """
    if not metadata:
        return metadata
    sanitized: Dict[str, str] = {}
    for key, value in metadata.items():
        if key in LITELLM_PROXY_INTERNAL_METADATA_KEYS:
            continue
        if isinstance(value, str):
            sanitized[key] = value
        else:
            verbose_proxy_logger.debug(
                "sanitize_openai_provider_metadata: dropping key %r with non-string value of type %s",
                key,
                type(value).__name__,
            )
    return sanitized or None

