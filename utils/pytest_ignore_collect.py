
def pytest_ignore_collect(collection_path: Path, config: Config) -> bool | None:
    """Return ``True`` to ignore this path for collection.

    Return ``None`` to let other plugins ignore the path for collection.

    Returning ``False`` will forcefully *not* ignore this path for collection,
    without giving a chance for other plugins to ignore this path.

    This hook is consulted for all files and directories prior to calling
    more specific hooks.

    Stops at first non-None result, see :ref:`firstresult`.

    :param collection_path: The path to analyze.
    :type collection_path: pathlib.Path
    :param config: The pytest config object.

    .. versionchanged:: 7.0.0
        The ``collection_path`` parameter was added as a :class:`pathlib.Path`
        equivalent of the ``path`` parameter. The ``path`` parameter
        has been deprecated and removed in pytest 9.0.0.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given collection path, only
    conftest files in parent directories of the collection path are consulted
    (if the path is a directory, its own conftest file is *not* consulted - a
    directory cannot ignore itself!).
    """


def pytest_ignore_collect(collection_path: Path, config: Config) -> bool | None:
    if collection_path.name == "__pycache__":
        return True

    ignore_paths = config._getconftest_pathlist(
        "collect_ignore", path=collection_path.parent
    )
    ignore_paths = ignore_paths or []
    excludeopt = config.getoption("ignore")
    if excludeopt:
        ignore_paths.extend(absolutepath(x) for x in excludeopt)

    if collection_path in ignore_paths:
        return True

    ignore_globs = config._getconftest_pathlist(
        "collect_ignore_glob", path=collection_path.parent
    )
    ignore_globs = ignore_globs or []
    excludeglobopt = config.getoption("ignore_glob")
    if excludeglobopt:
        ignore_globs.extend(absolutepath(x) for x in excludeglobopt)

    if any(fnmatch.fnmatch(str(collection_path), str(glob)) for glob in ignore_globs):
        return True

    allow_in_venv = config.getoption("collect_in_virtualenv")
    if not allow_in_venv and _in_venv(collection_path):
        return True

    if collection_path.is_dir():
        norecursepatterns = config.getini("norecursedirs")
        if any(fnmatch_ex(pat, collection_path) for pat in norecursepatterns):
            return True

    return None

