
def pytest_internalerror(
    excrepr: ExceptionRepr,
    excinfo: ExceptionInfo[BaseException],
) -> bool | None:
    """Called for internal errors.

    Return True to suppress the fallback handling of printing an
    INTERNALERROR message directly to sys.stderr.

    :param excrepr: The exception repr object.
    :param excinfo: The exception info.

    Use in conftest plugins
    =======================

    Any conftest plugin can implement this hook.
    """

