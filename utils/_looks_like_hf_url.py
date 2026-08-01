
def _looks_like_hf_url(uri: str, endpoint: str | None = None) -> bool:
    """Return True if 'uri' looks like a (possibly scheme-less) Hugging Face web URL."""
    lowered = uri.lower()
    if lowered.startswith(("http://", "https://")):
        return True
    # Scheme-less host (e.g. 'huggingface.co/org/model').
    return any(lowered == host or lowered.startswith(host + "/") for host in _recognized_hosts(endpoint))

