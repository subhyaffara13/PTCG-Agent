
def _get_sequence(
    d: Mapping[str, Any], expected_item_type: type[_T], key: str
) -> Sequence[_T] | None:
    """Get a list value from the dictionary and verify it's the expected items type."""
    if (value := _get(d, Sequence, key)) is None:  # type: ignore[type-abstract]
        return None
    if isinstance(value, (str, bytes)):
        # special case: str and bytes are Sequences, but we want to reject it
        raise PylockValidationError(
            f"Unexpected type {type(value).__name__} (expected Sequence)",
            context=key,
        )
    for i, item in enumerate(value):
        if not isinstance(item, expected_item_type):
            raise PylockValidationError(
                f"Unexpected type {type(item).__name__} "
                f"(expected {expected_item_type.__name__})",
                context=f"{key}[{i}]",
            )
    return value


def _get_sequence(
    d: Mapping[str, Any], expected_item_type: type[_T], key: str
) -> Sequence[_T] | None:
    """Get a list value from the dictionary and verify it's the expected items type."""
    if (value := _get(d, Sequence, key)) is None:  # type: ignore[type-abstract]
        return None
    if isinstance(value, (str, bytes)):
        # special case: str and bytes are Sequences, but we want to reject it
        raise PylockValidationError(
            f"Unexpected type {type(value).__name__} (expected Sequence)",
            context=key,
        )
    for i, item in enumerate(value):
        if not isinstance(item, expected_item_type):
            raise PylockValidationError(
                f"Unexpected type {type(item).__name__} "
                f"(expected {expected_item_type.__name__})",
                context=f"{key}[{i}]",
            )
    return value


def _get_sequence(
    d: Mapping[str, Any], expected_item_type: type[_T], key: str
) -> Sequence[_T] | None:
    """Get a list value from the dictionary and verify it's the expected items type."""
    if (value := _get(d, Sequence, key)) is None:  # type: ignore[type-abstract]
        return None
    if isinstance(value, (str, bytes)):
        # special case: str and bytes are Sequences, but we want to reject it
        raise PylockValidationError(
            f"Unexpected type {type(value).__name__} (expected Sequence)",
            context=key,
        )
    for i, item in enumerate(value):
        if not isinstance(item, expected_item_type):
            raise PylockValidationError(
                f"Unexpected type {type(item).__name__} "
                f"(expected {expected_item_type.__name__})",
                context=f"{key}[{i}]",
            )
    return value

