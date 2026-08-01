
def _int_or_none(value: str | None) -> int | None:
    try:
        return int(value)  # type: ignore
    except (TypeError, ValueError):
        return None

