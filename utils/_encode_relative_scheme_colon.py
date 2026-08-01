
def _encode_relative_scheme_colon(path: str) -> str:
    """Re-encode a scheme-shaped leading ``:`` in a relative path to ``%3A``."""
    colon_pos = path.find(":")
    if colon_pos <= 0:
        return path
    for c in path[:colon_pos]:
        if c not in _SCHEME_CHARS:
            return path
    return path[:colon_pos] + "%3A" + path[colon_pos + 1 :]

