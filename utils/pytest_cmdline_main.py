
def pytest_cmdline_main(config: Config) -> int | ExitCode | None:
    if config.option.cacheshow and not config.option.help:
        from _pytest.main import wrap_session

        return wrap_session(config, cacheshow)
    return None


def pytest_cmdline_main(config: Config) -> int | ExitCode | None:
    if config.option.showfixtures:
        showfixtures(config)
        return 0
    if config.option.show_fixtures_per_test:
        show_fixtures_per_test(config)
        return 0
    return None


def pytest_cmdline_main(config: Config) -> int | ExitCode | None:
    # Note: a single `--version` argument is handled directly by `Config.main()` to avoid starting up the entire
    # pytest infrastructure just to display the version (#13574).
    if config.option.version > 1:
        show_version_verbose(config)
        return ExitCode.OK
    elif config.option.help:
        config._do_configure()
        showhelp(config)
        config._ensure_unconfigure()
        return ExitCode.OK
    return None


def pytest_cmdline_main(config: Config) -> ExitCode | int | None:
    """Called for performing the main command line action.

    The default implementation will invoke the configure hooks and
    :hook:`pytest_runtestloop`.

    Stops at first non-None result, see :ref:`firstresult`.

    :param config: The pytest config object.
    :returns: The exit code.

    Use in conftest plugins
    =======================

    This hook is only called for :ref:`initial conftests <pluginorder>`.
    """


def pytest_cmdline_main(config: Config) -> int | ExitCode:
    return wrap_session(config, _main)


def pytest_cmdline_main(config: Config) -> int | ExitCode | None:
    if config.option.setuponly:
        config.option.setupshow = True
    return None


def pytest_cmdline_main(config: Config) -> int | ExitCode | None:
    if config.option.setupplan:
        config.option.setuponly = True
        config.option.setupshow = True
    return None


def pytest_cmdline_main(config: Config) -> int | ExitCode | None:
    import _pytest.config

    if config.option.markers:
        config._do_configure()
        tw = _pytest.config.create_terminal_writer(config)
        for line in config.getini("markers"):
            parts = line.split(":", 1)
            name = parts[0]
            rest = parts[1] if len(parts) == 2 else ""
            tw.write(f"@pytest.mark.{name}:", bold=True)
            tw.line(rest)
            tw.line()
        config._ensure_unconfigure()
        return 0

    return None


def pytest_cmdline_main(config: pytest.Config) -> None:
    if config.getoption("--collectonly"):
        return
    # --update-data is not compatible with parallelized tests, disable parallelization
    if config.getoption("--update-data"):
        config.option.numprocesses = 0

