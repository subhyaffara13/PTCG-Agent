
def _is_openai_compatible_url(url_route: Optional[str]) -> bool:
    """True if the URL targets an OpenAI-compatible API surface.

    For the shared Azure Cognitive Services domains we additionally require an
    OpenAI-style path segment (`/openai/` or `/v1/`) so non-OpenAI Azure services
    (Speech, Vision, Language, ...) on the same domain are not misclassified as
    OpenAI routes.
    """
    if not url_route:
        return False
    parsed_url = urlparse(url_route)
    hostname = parsed_url.hostname
    if not hostname:
        return False
    if _hostname_matches(hostname, _OPENAI_HOSTNAMES):
        return True
    if _hostname_matches(hostname, _AZURE_OPENAI_HOSTNAMES):
        return any(marker in parsed_url.path for marker in _AZURE_OPENAI_PATH_MARKERS)
    return False

