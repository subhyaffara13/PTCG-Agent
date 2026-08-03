from pathlib import Path


def pytest_collect_directory(path: Path, parent: Collector) -> Collector | None:
    """Create a :class:`~pytest.Collector` for the given directory, or None if
    not relevant.

    .. versionadded:: 8.0

    For best results, the returned collector should be a subclass of
    :class:`~pytest.Directory`, but this is not required.

    The new node needs to have the specified ``parent`` as a parent.

    Stops at first non-None result, see :ref:`firstresult`.

    :param path: The path to analyze.
    :type path: pathlib.Path

    See :ref:`custom directory collectors` for a simple example of use of this
    hook.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given collection path, only
    conftest files in parent directories of the collection path are consulted
    (if the path is a directory, its own conftest file is *not* consulted - a
    directory cannot collect itself!).
    """


def pytest_collect_directory(
    path: Path, parent: nodes.Collector
) -> nodes.Collector | None:
    return Dir.from_parent(parent, path=path)


def pytest_collect_directory(
    path: Path, parent: nodes.Collector
) -> nodes.Collector | None:
    pkginit = path / "__init__.py"
    try:
        has_pkginit = pkginit.is_file()
    except PermissionError:
        # See https://github.com/pytest-dev/pytest/issues/12120#issuecomment-2106349096.
        return None
    if has_pkginit:
        return Package.from_parent(parent, path=path)
    return None

