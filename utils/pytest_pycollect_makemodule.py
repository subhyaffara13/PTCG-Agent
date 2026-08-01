
def pytest_pycollect_makemodule(module_path: Path, parent) -> Module | None:
    """Return a :class:`pytest.Module` collector or None for the given path.

    This hook will be called for each matching test module path.
    The :hook:`pytest_collect_file` hook needs to be used if you want to
    create test modules for files that do not match as a test module.

    Stops at first non-None result, see :ref:`firstresult`.

    :param module_path: The path of the module to collect.
    :type module_path: pathlib.Path

    .. versionchanged:: 7.0.0
        The ``module_path`` parameter was added as a :class:`pathlib.Path`
        equivalent of the ``path`` parameter. The ``path`` parameter has been
        deprecated in favor of ``module_path`` and removed in pytest 9.0.0.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given parent collector,
    only conftest files in the collector's directory and its parent directories
    are consulted.
    """


def pytest_pycollect_makemodule(module_path: Path, parent) -> Module:
    return Module.from_parent(parent, path=module_path)

