
def pytest_markeval_namespace(  # type:ignore[empty-body]
    config: Config,
) -> dict[str, Any]:
    """Called when constructing the globals dictionary used for
    evaluating string conditions in xfail/skipif markers.

    This is useful when the condition for a marker requires
    objects that are expensive or impossible to obtain during
    collection time, which is required by normal boolean
    conditions.

    .. versionadded:: 6.2

    :param config: The pytest config object.
    :returns: A dictionary of additional globals to add.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given item, only conftest
    files in parent directories of the item are consulted.
    """

