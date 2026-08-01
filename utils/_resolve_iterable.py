
def _resolve_iterable(iterable: str | Iterable[str] | None) -> Iterable[str]:
    """
    Resolve various input types to a consistent iterable of strings.

    Args:
        iterable: String, iterable of strings, or None

    Returns:
        Iterable[str]: Consistent iterable output
    """
    if iterable is None:
        return []

    if not isinstance(iterable, Iterable) or isinstance(iterable, str):
        return (iterable,)

    return iterable

