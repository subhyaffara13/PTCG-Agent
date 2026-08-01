
def _format_deprecated_suffix(deprecated: bool | str) -> str:
    """Return the trailing reason for a ``DeprecationWarning`` message,
    prefixed with a space, or an empty string when no reason was given.
    """
    if isinstance(deprecated, str):
        return f" {deprecated}"
    return ""

