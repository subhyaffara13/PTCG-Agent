
def _translate_key(key: str) -> str:
    """
    if `key` is deprecated and a replacement key defined, will return the
    replacement key, otherwise returns `key` as-is
    """
    d = _get_deprecated_option(key)
    if d:
        return d.rkey or key
    else:
        return key

