
def _extract_credential_from_entry(
    entry: dict, provider: Optional[str] = None
) -> Optional[str]:
    """
    Extract litellm_credentials from a model_config entry.

    Entry structure: {"azure": {"litellm_credentials": "name"}, ...}

    When provider is given (e.g. "azure"), tries an exact provider match first.
    Falls back to the first credential found across all provider keys.
    """
    if not isinstance(entry, dict):
        return None

    # Prefer exact provider match when provider hint is available
    if provider and provider in entry:
        provider_config = entry[provider]
        if isinstance(provider_config, dict):
            credential_name = provider_config.get("litellm_credentials")
            if credential_name:
                return credential_name

    # Fall back to first available provider
    for provider_config in entry.values():
        if isinstance(provider_config, dict):
            credential_name = provider_config.get("litellm_credentials")
            if credential_name:
                return credential_name
    return None

