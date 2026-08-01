
def _get_required_as(
    d: Mapping[str, Any],
    expected_type: type[_T],
    target_type: Callable[[_T], _T2],
    key: str,
) -> _T2:
    """Get a required value from the dict, verify it's the expected type,
    and convert to the target type."""
    if (value := _get_as(d, expected_type, target_type, key)) is None:
        raise _PylockRequiredKeyError(key)
    return value


def _get_required_as(
    d: Mapping[str, Any],
    expected_type: type[_T],
    target_type: Callable[[_T], _T2],
    key: str,
) -> _T2:
    """Get a required value from the dict, verify it's the expected type,
    and convert to the target type."""
    if (value := _get_as(d, expected_type, target_type, key)) is None:
        raise _PylockRequiredKeyError(key)
    return value


def _get_required_as(
    d: Mapping[str, Any],
    expected_type: type[_T],
    target_type: Callable[[_T], _T2],
    key: str,
) -> _T2:
    """Get a required value from the dict, verify it's the expected type,
    and convert to the target type."""
    if (value := _get_as(d, expected_type, target_type, key)) is None:
        raise _PylockRequiredKeyError(key)
    return value

