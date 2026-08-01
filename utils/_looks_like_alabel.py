
def _looks_like_alabel(s: str) -> bool:
    """Return True if any label in ``s`` carries the ``xn--`` ACE prefix."""
    prefix = _alabel_prefix.decode("ascii")
    return any(label.lower().startswith(prefix) for label in _unicode_dots_re.split(s))

