
def _missing_canonicalize_license_expression(expression: str) -> str:
    """
    Defer import error to affect only users that actually use it
    https://github.com/pypa/setuptools/issues/4894
    >>> _missing_canonicalize_license_expression("a OR b")
    Traceback (most recent call last):
    ...
    ImportError: ...Cannot import `packaging.licenses`...
    """
    raise ImportError(
        "Cannot import `packaging.licenses`."
        """
        Setuptools>=77.0.0 requires "packaging>=24.2" to work properly.
        Please make sure you have a suitable version installed.
        """
    )

