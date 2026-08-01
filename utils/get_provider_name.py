
def get_provider_name(provider: str) -> str:
    """
    Resolve provider aliases to canonical provider names.

    Args:
        provider: Provider name (may be an alias)

    Returns:
        Canonical provider name
    """
    config = _load_beta_headers_config()
    aliases = config.get("provider_aliases", {})
    return aliases.get(provider, provider)

