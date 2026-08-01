
def safe_repr(obj: Any) -> str:
    try:
        return repr(obj)
    except Exception:  # pylint: disable=broad-except
        return "???"

