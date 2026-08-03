from pathlib import Path


def pytest_collect_file(
    file_path: Path,
    parent: Collector,
) -> DoctestModule | DoctestTextfile | None:
    config = parent.config
    if file_path.suffix == ".py":
        if config.option.doctestmodules and not any(
            (_is_setup_py(file_path), _is_main_py(file_path))
        ):
            return DoctestModule.from_parent(parent, path=file_path)
    elif _is_doctest(config, file_path, parent):
        return DoctestTextfile.from_parent(parent, path=file_path)
    return None


def pytest_collect_file(file_path: Path, parent: Collector) -> Collector | None:
    """Create a :class:`~pytest.Collector` for the given path, or None if not relevant.

    For best results, the returned collector should be a subclass of
    :class:`~pytest.File`, but this is not required.

    The new node needs to have the specified ``parent`` as a parent.

    :param file_path: The path to analyze.
    :type file_path: pathlib.Path

    .. versionchanged:: 7.0.0
        The ``file_path`` parameter was added as a :class:`pathlib.Path`
        equivalent of the ``path`` parameter. The ``path`` parameter
        has been deprecated and removed in pytest 9.0.0.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given file path, only
    conftest files in parent directories of the file path are consulted.
    """


def pytest_collect_file(file_path: Path, parent: nodes.Collector) -> Module | None:
    if file_path.suffix == ".py":
        if not parent.session.isinitpath(file_path):
            if not path_matches_patterns(
                file_path, parent.config.getini("python_files")
            ):
                return None
        ihook = parent.session.gethookproxy(file_path)
        module: Module = ihook.pytest_pycollect_makemodule(
            module_path=file_path, parent=parent
        )
        return module
    return None

