
def _is_master_key(api_key: Optional[str], _master_key: Optional[str]) -> bool:
    """
    Raw-only constant-time master-key comparison. The hashed form is never
    considered equivalent — only the raw master-key string matches.
    """
    if _master_key is None or api_key is None:
        return False
    return secrets.compare_digest(api_key, _master_key)

