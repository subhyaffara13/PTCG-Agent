
def _endpoint_matches_api_base(endpoint: str, api_base: str) -> bool:
    """
    Match a registered openai-compatible endpoint against a caller-supplied
    ``api_base`` using parsed-URL semantics, not unanchored substring search.

    Both inputs may be a bare hostname (``api.perplexity.ai``), host+path
    (``api.deepinfra.com/v1/openai``), or a full URL
    (``https://api.cerebras.ai/v1``). Hostnames must match exactly
    (case-insensitive); if the registered endpoint has a non-trivial path,
    the api_base path must start with it on a segment boundary.

    The naive ``endpoint in api_base`` shape lets a caller pass
    ``https://attacker.com/api.groq.com/openai/v1`` to coerce the proxy
    into reading the server's GROQ_API_KEY from the environment and
    forwarding it to the attacker's host as a Bearer credential.
    """

    def _parse(value: str):
        # Ensure urlparse sees a scheme so it populates hostname / path.
        normalized = value if "://" in value else f"https://{value}"
        return urlparse(normalized)

    parsed_endpoint = _parse(endpoint)
    parsed_url = _parse(api_base)

    endpoint_host = (parsed_endpoint.hostname or "").lower()
    url_host = (parsed_url.hostname or "").lower()
    if not endpoint_host or endpoint_host != url_host:
        return False

    endpoint_path = parsed_endpoint.path.rstrip("/")
    if not endpoint_path:
        return True
    url_path = parsed_url.path.rstrip("/")
    return url_path == endpoint_path or url_path.startswith(endpoint_path + "/")

