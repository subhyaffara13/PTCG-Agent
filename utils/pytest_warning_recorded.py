
def pytest_warning_recorded(
    warning_message: warnings.WarningMessage,
    when: Literal["config", "collect", "runtest"],
    nodeid: str,
    location: tuple[str, int, str] | None,
) -> None:
    """Process a warning captured by the internal pytest warnings plugin.

    :param warning_message:
        The captured warning. This is the same object produced by :class:`warnings.catch_warnings`,
        and contains the same attributes as the parameters of :py:func:`warnings.showwarning`.

    :param when:
        Indicates when the warning was captured. Possible values:

        * ``"config"``: during pytest configuration/initialization stage.
        * ``"collect"``: during test collection.
        * ``"runtest"``: during test execution.

    :param nodeid:
        Full id of the item. Empty string for warnings that are not specific to
        a particular node.

    :param location:
        When available, holds information about the execution context of the captured
        warning (filename, linenumber, function). ``function`` evaluates to <module>
        when the execution context is at the module level.

    .. versionadded:: 6.0

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. If the warning is specific to a
    particular node, only conftest files in parent directories of the node are
    consulted.
    """

