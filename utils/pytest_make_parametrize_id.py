
def pytest_make_parametrize_id(config: Config, val: object, argname: str) -> str | None:
    """Return a user-friendly string representation of the given ``val``
    that will be used by @pytest.mark.parametrize calls, or None if the hook
    doesn't know about ``val``.

    The parameter name is available as ``argname``, if required.

    Stops at first non-None result, see :ref:`firstresult`.

    :param config: The pytest config object.
    :param val: The parametrized value.
    :param argname: The automatic parameter name produced by pytest.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook.
    """

