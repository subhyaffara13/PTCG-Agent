
def error_of_type(
    handler: nodes.ExceptHandler,
    error_type: str | type[Exception] | tuple[str | type[Exception], ...],
) -> bool:
    """Check if the given exception handler catches
    the given error_type.

    The *handler* parameter is a node, representing an ExceptHandler node.
    The *error_type* can be an exception, such as AttributeError,
    the name of an exception, or it can be a tuple of errors.
    The function will return True if the handler catches any of the
    given errors.
    """

    def stringify_error(error: str | type[Exception]) -> str:
        if not isinstance(error, str):
            return error.__name__
        return error

    if not isinstance(error_type, tuple):
        error_type = (error_type,)
    expected_errors = {stringify_error(error) for error in error_type}
    if not handler.type:
        return False
    return handler.catch(expected_errors)  # type: ignore[no-any-return]

