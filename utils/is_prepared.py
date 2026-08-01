
def is_prepared(request: PreparedRequest) -> TypeIs[_ValidatedRequest]:
    """Verify a PreparedRequest has been fully prepared."""
    if TYPE_CHECKING:
        return request.url is not None and request.method is not None
    # noop at runtime to avoid AssertionError
    return True

