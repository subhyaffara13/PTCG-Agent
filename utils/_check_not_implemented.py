
def _check_not_implemented(cond, message=None):  # noqa: F811
    r"""Throws error containing an optional message if the specified condition
    is False.

    Error type: ``NotImplementedError``

    C++ equivalent: ``TORCH_CHECK_NOT_IMPLEMENTED``

    Args:
        cond (:class:`bool`): If False, throw error

        message (Callable, optional): Callable that returns either a string or
            an object that has a ``__str__()`` method to be used as the error
            message. Default: ``None``
    """
    _check_with(
        NotImplementedError,
        cond,
        # pyrefly: ignore [bad-argument-type]
        message,
    )

