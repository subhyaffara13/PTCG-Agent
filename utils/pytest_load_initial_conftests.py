import sys

def pytest_load_initial_conftests(early_config: Config) -> Generator[None]:
    ns = early_config.known_args_namespace
    if ns.capture == "fd":
        _windowsconsoleio_workaround(sys.stdout)
    _colorama_workaround()
    _readline_workaround()
    pluginmanager = early_config.pluginmanager
    capman = CaptureManager(ns.capture)
    pluginmanager.register(capman, "capturemanager")

    # Make sure that capturemanager is properly reset at final shutdown.
    early_config.add_cleanup(capman.stop_global_capturing)

    # Finally trigger conftest loading but while capturing (issue #93).
    capman.start_global_capturing()
    try:
        try:
            yield
        finally:
            capman.suspend_global_capture()
    except BaseException:
        out, err = capman.read_global_capture()
        sys.stdout.write(out)
        sys.stderr.write(err)
        raise


def pytest_load_initial_conftests(
    early_config: Config, parser: Parser, args: list[str]
) -> None:
    """Called to implement the loading of :ref:`initial conftest files
    <pluginorder>` ahead of command line option parsing.

    :param early_config: The pytest config object.
    :param args: Arguments passed on the command line.
    :param parser: To add command line options.

    Use in conftest plugins
    =======================

    This hook is not called for conftest files.
    """


def pytest_load_initial_conftests(early_config: Config) -> None:
    """Monkeypatch legacy path attributes in several classes, as early as possible."""
    mp = MonkeyPatch()
    early_config.add_cleanup(mp.undo)

    # Add Cache.makedir().
    mp.setattr(Cache, "makedir", Cache_makedir, raising=False)

    # Add FixtureRequest.fspath property.
    mp.setattr(FixtureRequest, "fspath", property(FixtureRequest_fspath), raising=False)

    # Add TerminalReporter.startdir property.
    mp.setattr(
        TerminalReporter, "startdir", property(TerminalReporter_startdir), raising=False
    )

    # Add Config.{invocation_dir,rootdir,inifile} properties.
    mp.setattr(Config, "invocation_dir", property(Config_invocation_dir), raising=False)
    mp.setattr(Config, "rootdir", property(Config_rootdir), raising=False)
    mp.setattr(Config, "inifile", property(Config_inifile), raising=False)

    # Add Session.startdir property.
    mp.setattr(Session, "startdir", property(Session_startdir), raising=False)

    # Add pathlist configuration type.
    mp.setattr(Config, "_getini_unknown_type", Config__getini_unknown_type)

    # Add Node.fspath property.
    mp.setattr(Node, "fspath", property(Node_fspath, Node_fspath_set), raising=False)


def pytest_load_initial_conftests(
    early_config: Config,
) -> Generator[None]:
    with catch_warnings_for_item(
        config=early_config, ihook=early_config.hook, when="config", item=None
    ):
        return (yield)

