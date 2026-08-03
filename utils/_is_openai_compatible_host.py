from typing import Optional

def _is_openai_compatible_host(hostname: Optional[str]) -> bool:
    """True if the hostname is OpenAI proper or one of the Azure OpenAI domains.

    Hostname-only check, kept for the route-level helpers that additionally
    require a specific OpenAI path (e.g. `/v1/chat/completions`). When only the
    hostname would otherwise gate dispatch, use `_is_openai_compatible_url` so
    non-OpenAI Azure Cognitive Services on the shared domains are excluded.
    """
    if not hostname:
        return False
    return _hostname_matches(hostname, _OPENAI_HOSTNAMES) or _hostname_matches(
        hostname, _AZURE_OPENAI_HOSTNAMES
    )

