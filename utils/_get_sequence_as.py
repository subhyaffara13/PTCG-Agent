
def _get_sequence_as(
    d: Mapping[str, Any],
    expected_item_type: type[_T],
    target_item_type: Callable[[_T], _T2],
    key: str,
) -> list[_T2] | None:
    """Get list value from dictionary and verify expected items type."""
    if (value := _get_sequence(d, expected_item_type, key)) is None:
        return None
    result = []
    try:
        for item in value:
            typed_item = target_item_type(item)
            result.append(typed_item)
    except Exception as e:
        raise PylockValidationError(e, context=f"{key}[{len(result)}]") from e
    return result


def _get_sequence_as(
    d: Mapping[str, Any],
    expected_item_type: type[_T],
    target_item_type: Callable[[_T], _T2],
    key: str,
) -> list[_T2] | None:
    """Get list value from dictionary and verify expected items type."""
    if (value := _get_sequence(d, expected_item_type, key)) is None:
        return None
    result = []
    try:
        for item in value:
            typed_item = target_item_type(item)
            result.append(typed_item)
    except Exception as e:
        raise PylockValidationError(e, context=f"{key}[{len(result)}]") from e
    return result


def _get_sequence_as(
    d: Mapping[str, Any],
    expected_item_type: type[_T],
    target_item_type: Callable[[_T], _T2],
    key: str,
) -> list[_T2] | None:
    """Get list value from dictionary and verify expected items type."""
    if (value := _get_sequence(d, expected_item_type, key)) is None:
        return None
    result = []
    try:
        for item in value:
            typed_item = target_item_type(item)
            result.append(typed_item)
    except Exception as e:
        raise PylockValidationError(e, context=f"{key}[{len(result)}]") from e
    return result

