
def pytest_report_header(config):
    del config  # Unused.
    assert (
        pybind11_tests.compiler_info is not None
    ), "Please update pybind11_tests.cpp if this assert fails."
    return (
        "C++ Info:"
        f" {pybind11_tests.compiler_info}"
        f" {pybind11_tests.cpp_std}"
        f" {pybind11_tests.PYBIND11_INTERNALS_ID}"
        f" PYBIND11_SIMPLE_GIL_MANAGEMENT={pybind11_tests.PYBIND11_SIMPLE_GIL_MANAGEMENT}"
    )


def pytest_report_header(config):
    s = "architecture: %s\n" % ARCH
    s += "cache:        %s\n" % USE_CACHE
    version = ""
    if GROUND_TYPES == "gmpy":
        import gmpy2

        version = gmpy2.version()
    elif GROUND_TYPES == "flint":
        try:
            from flint import __version__
        except ImportError:
            version = "unknown"
        else:
            version = f'(python-flint=={__version__})'
    s += "ground types: %s %s\n" % (GROUND_TYPES, version)
    return s


def pytest_report_header(config: Config) -> str | None:
    """Display cachedir with --cache-show and if non-default."""
    if config.option.verbose > 0 or config.getini("cache_dir") != ".pytest_cache":
        assert config.cache is not None
        cachedir = config.cache._cachedir
        # TODO: evaluate generating upward relative paths
        # starting with .., ../.. if sensible

        try:
            displaypath = cachedir.relative_to(config.rootpath)
        except ValueError:
            displaypath = cachedir
        return f"cachedir: {displaypath}"
    return None


def pytest_report_header(config: Config) -> list[str]:
    lines = []
    if config.option.debug or config.option.traceconfig:
        lines.append(f"using: pytest-{pytest.__version__}")

        verinfo = getpluginversioninfo(config)
        if verinfo:
            lines.extend(verinfo)

    if config.option.traceconfig:
        lines.append("active plugins:")
        items = config.pluginmanager.list_name_plugin()
        for name, plugin in items:
            if hasattr(plugin, "__file__"):
                r = plugin.__file__
            else:
                r = repr(plugin)
            lines.append(f"    {name:<20}: {r}")
    return lines


def pytest_report_header(config: Config, start_path: Path) -> str | list[str]:  # type: ignore[empty-body]
    """Return a string or list of strings to be displayed as header info for terminal reporting.

    :param config: The pytest config object.
    :param start_path: The starting dir.
    :type start_path: pathlib.Path

    .. note::

        Lines returned by a plugin are displayed before those of plugins which
        ran before it.
        If you want to have your line(s) displayed first, use
        :ref:`trylast=True <plugin-hookorder>`.

    .. versionchanged:: 7.0.0
        The ``start_path`` parameter was added as a :class:`pathlib.Path`
        equivalent of the ``startdir`` parameter. The ``startdir`` parameter
        has been deprecated and removed in pytest 9.0.0.

    Use in conftest plugins
    =======================

    This hook is only called for :ref:`initial conftests <pluginorder>`.
    """

