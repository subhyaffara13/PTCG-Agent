
def convert_attrs(value: Any) -> Any:
    """Convert Token.attrs set as ``None`` or ``[[key, value], ...]`` to a dict.

    This improves compatibility with upstream markdown-it.
    """
    if not value:
        return {}
    if isinstance(value, list):
        return dict(value)
    return value

