
def _safe_repr(v: Any) -> int | float | str:
    """The context argument for `PydanticKnownError` requires a number or str type, so we do a simple repr() coercion for types like timedelta.

    See tests/test_types.py::test_annotated_metadata_any_order for some context.
    """
    if isinstance(v, (int, float, str)):
        return v
    return repr(v)

