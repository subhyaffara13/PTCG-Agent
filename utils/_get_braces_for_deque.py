
def _get_braces_for_deque(_object: Deque[Any]) -> Tuple[str, str, str]:
    if _object.maxlen is None:
        return ("deque([", "])", "deque()")
    return (
        "deque([",
        f"], maxlen={_object.maxlen})",
        f"deque(maxlen={_object.maxlen})",
    )


def _get_braces_for_deque(_object: Deque[Any]) -> Tuple[str, str, str]:
    if _object.maxlen is None:
        return ("deque([", "])", "deque()")
    return (
        "deque([",
        f"], maxlen={_object.maxlen})",
        f"deque(maxlen={_object.maxlen})",
    )

