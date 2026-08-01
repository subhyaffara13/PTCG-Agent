
def pytest_cmdline_parse() -> Generator[None, Config, Config]:
    config = yield

    if config.option.debug:
        # --debug | --debug <file.log> was provided.
        path = config.option.debug
        debugfile = open(path, "w", encoding="utf-8")
        debugfile.write(
            "versions pytest-{}, "
            "python-{}\ninvocation_dir={}\ncwd={}\nargs={}\n\n".format(
                pytest.__version__,
                ".".join(map(str, sys.version_info)),
                config.invocation_params.dir,
                os.getcwd(),
                config.invocation_params.args,
            )
        )
        config.trace.root.setwriter(debugfile.write)
        undo_tracing = config.pluginmanager.enable_tracing()
        sys.stderr.write(f"writing pytest debug information to {path}\n")

        def unset_tracing() -> None:
            debugfile.close()
            sys.stderr.write(f"wrote pytest debug information to {debugfile.name}\n")
            config.trace.root.setwriter(None)
            undo_tracing()

        config.add_cleanup(unset_tracing)

    return config


def pytest_cmdline_parse(
    pluginmanager: PytestPluginManager, args: list[str]
) -> Config | None:
    """Return an initialized :class:`~pytest.Config`, parsing the specified args.

    Stops at first non-None result, see :ref:`firstresult`.

    .. note::
        This hook is only called for plugin classes passed to the
        ``plugins`` arg when using `pytest.main`_ to perform an in-process
        test run.

    :param pluginmanager: The pytest plugin manager.
    :param args: List of arguments passed on the command line.
    :returns: A pytest config object.

    Use in conftest plugins
    =======================

    This hook is not called for conftest files.
    """

