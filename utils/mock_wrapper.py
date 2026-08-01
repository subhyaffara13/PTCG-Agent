
def mock_wrapper(method):
    """
    Returns a function that calls the real implementation of a method
    in addition to passing args to a mock object.
    """
    mock = MagicMock()

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        mock(*args, **kwargs)
        return method(self, *args, **kwargs)
    wrapper.mock = mock  # type: ignore[attr-defined]
    return wrapper

