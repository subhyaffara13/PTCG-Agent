
def _safe_has_attribute(obj, member: str) -> bool:
    """Required because unexpected RunTimeError can be raised.

    See https://github.com/pylint-dev/astroid/issues/1958
    """
    try:
        return hasattr(obj, member)
    except Exception:  # pylint: disable=broad-except
        return False

