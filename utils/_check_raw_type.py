
def _check_raw_type(
    expected_type: type[BaseException] | tuple[type[BaseException], ...] | None,
    exception: BaseException,
) -> str | None:
    if expected_type is None or expected_type == ():
        return None

    if not isinstance(
        exception,
        expected_type,
    ):
        actual_type_str = backquote(_exception_type_name(type(exception)) + "()")
        expected_type_str = backquote(_exception_type_name(expected_type))
        if (
            isinstance(exception, BaseExceptionGroup)
            and isinstance(expected_type, type)
            and not issubclass(expected_type, BaseExceptionGroup)
        ):
            return f"Unexpected nested {actual_type_str}, expected {expected_type_str}"
        return f"{actual_type_str} is not an instance of {expected_type_str}"
    return None

