
def maybe_transform(
    data: object,
    expected_type: object,
) -> Any | None:
    """Wrapper over `transform()` that allows `None` to be passed.

    See `transform()` for more details.
    """
    if data is None:
        return None
    return transform(data, expected_type)

