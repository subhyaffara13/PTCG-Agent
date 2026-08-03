from typing import Optional

def infer_openai_data_residency(
    custom_llm_provider: Optional[str], api_base: Optional[str]
) -> Optional[str]:
    """
    Derive the OpenAI data-residency region from an api_base URL.

    Returns ``"eu"`` for the EU regional host, ``"us"`` for the US regional
    host, and ``None`` for the default global host, any non-OpenAI provider,
    or any non-OpenAI URL.
    """
    if custom_llm_provider != "openai" or not api_base:
        return None
    try:
        host = urlparse(api_base).hostname
    except (TypeError, ValueError):
        return None
    if not host:
        return None
    return _OPENAI_REGIONAL_HOSTS.get(host.lower())

