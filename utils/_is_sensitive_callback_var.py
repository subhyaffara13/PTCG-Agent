
def _is_sensitive_callback_var(key: str) -> bool:
    """Match codebase precedent: only credential-bearing fields get encrypted;
    routing/identifier fields (host, base_url, project, region) stay plain."""
    if key in _EXTRA_SENSITIVE_CALLBACK_KEYS:
        return True
    return _CALLBACK_VAR_MASKER.is_sensitive_key(key)

