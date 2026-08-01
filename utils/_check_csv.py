
def _check_csv(value: list[str] | tuple[str] | str) -> Sequence[str]:
    if isinstance(value, (list, tuple)):
        return value
    return _splitstrip(value)

