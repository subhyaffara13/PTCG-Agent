
def pytest_configure():
    pytest.suppress = contextlib.suppress
    pytest.gc_collect = gc_collect


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "anyio: mark the (coroutine function) test to be run asynchronously via anyio.",
    )
    if (
        config.getini("anyio_mode") == "auto"
        and config.pluginmanager.has_plugin("asyncio")
        and config.getini("asyncio_mode") == "auto"
    ):
        config.issue_config_time_warning(
            pytest.PytestConfigWarning(
                "AnyIO auto mode has been enabled together with pytest-asyncio auto "
                "mode. This may cause unexpected behavior."
            ),
            1,
        )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")
    backend = config.getoption("--backend")
    if backend is None:
        backend = os.environ.get("NETWORKX_TEST_BACKEND")
    # nx_loopback backend is only available when testing with a backend
    loopback_ep = entry_points(name="nx_loopback", group="networkx.backends")
    if not loopback_ep:
        warnings.warn(
            "\n\n             WARNING: Mixed NetworkX configuration! \n\n"
            "        This environment has mixed configuration for networkx.\n"
            "        The test object nx_loopback is not configured correctly.\n"
            "        You should not be seeing this message.\n"
            "        Try `pip install -e .`, or change your PYTHONPATH\n"
            "        Make sure python finds the networkx repo you are testing\n\n"
        )
    config.backend = backend
    if backend:
        # We will update `networkx.config.backend_priority` below in `*_modify_items`
        # to allow tests to get set up with normal networkx graphs.
        nx.utils.backends.backends["nx_loopback"] = loopback_ep["nx_loopback"]
        nx.utils.backends.backend_info["nx_loopback"] = {}
        nx.config.backends = nx.utils.Config(
            nx_loopback=nx.utils.Config(),
            **nx.config.backends,
        )
        fallback_to_nx = config.getoption("--fallback-to-nx")
        if not fallback_to_nx:
            fallback_to_nx = os.environ.get("NETWORKX_FALLBACK_TO_NX")
        nx.config.fallback_to_nx = bool(fallback_to_nx)
        nx.utils.backends._dispatchable.__call__ = (
            nx.utils.backends._dispatchable._call_if_any_backends_installed
        )


def pytest_configure(config):
    config.addinivalue_line("markers",
        "valgrind_error: Tests that are known to error under valgrind.")
    config.addinivalue_line("markers",
        "leaks_references: Tests that are known to leak references.")
    config.addinivalue_line("markers",
        "slow: Tests that are very slow.")
    if not PARALLEL_RUN_AVAILABLE:
        config.addinivalue_line("markers",
            "parallel_threads(n): run the given test function in parallel "
            "using `n` threads.",
        )
        config.addinivalue_line("markers",
            "iterations(n): run the given test function `n` times in each thread",
        )
        config.addinivalue_line("markers",
            "thread_unsafe: mark the test function as single-threaded",
        )


def pytest_configure(config):
    """
    Add pytest markers to avoid PytestUnknownMarkWarning

    This needs to contain all markers that are SciPy-specific, as well as
    dummy fallbacks for markers defined in optional test packages.

    Note that we need both the registration here *and* in `pytest.ini`.
    """
    config.addinivalue_line("markers",
        "slow: Tests that are very slow.")
    config.addinivalue_line("markers",
        "xslow: mark test as extremely slow (not run unless explicitly requested)")
    config.addinivalue_line("markers",
        "xfail_on_32bit: mark test as failing on 32-bit platforms")
    config.addinivalue_line("markers",
        "array_api_backends: test iterates on all array API backends")
    config.addinivalue_line("markers",
        ("skip_xp_backends(backends, reason=None, np_only=False, cpu_only=False, " +
         "eager_only=False, exceptions=None): mark the desired skip configuration " +
         "for the `skip_xp_backends` fixture"))
    config.addinivalue_line("markers",
        ("xfail_xp_backends(backends, reason=None, np_only=False, cpu_only=False, " +
         "eager_only=False, exceptions=None): mark the desired xfail configuration " +
         "for the `xfail_xp_backends` fixture"))
    config.addinivalue_line("markers",
                            ("uses_xp_capabilities(status, funcs=None, " +
                             "reason=None): mark " +
                            "whether pytest markers for array API backends are " +
                            " generated from the xp_capabilities entries for one or "
                             " more functions"))

    try:
        import pytest_timeout  # noqa:F401
    except Exception:
        config.addinivalue_line(
            "markers", 'timeout: mark a test for a non-default timeout')
    try:
        # This is a more reliable test of whether pytest_fail_slow is installed
        # When I uninstalled it, `import pytest_fail_slow` didn't fail!
        from pytest_fail_slow import parse_duration  # type: ignore[import-not-found] # noqa:F401,E501
    except Exception:
        config.addinivalue_line(
            "markers", 'fail_slow: mark a test for a non-default timeout failure')

    if not PARALLEL_RUN_AVAILABLE:
        config.addinivalue_line(
            'markers',
            'parallel_threads_limit(n): run the given test function in parallel '
            'using `n` threads.')
        config.addinivalue_line(
            "markers",
            "thread_unsafe: mark the test function as single-threaded",
        )
        config.addinivalue_line(
            "markers",
            "iterations(n): run the given test function `n` times in each thread",
        )

    if os.name == 'posix' and sys.version_info < (3, 14) and sys.platform != "cygwin":
        # On POSIX, Python 3.13 and older uses the 'fork' context by
        # default. Calling fork() from multiple threads leads to
        # deadlocks. This has been changed in 3.14 to 'forkserver'.
        multiprocessing.set_start_method('forkserver', force=True)


def pytest_configure(config: Config) -> None:
    """Configure cache system and register related plugins.

    Creates the Cache instance and registers the last-failed (LFPlugin)
    and new-first (NFPlugin) plugins with the plugin manager.

    :param config: pytest configuration object.
    """
    config.cache = Cache.for_config(config, _ispytest=True)
    config.pluginmanager.register(LFPlugin(config), "lfplugin")
    config.pluginmanager.register(NFPlugin(config), "nfplugin")


def pytest_configure(config: Config) -> None:
    import pdb

    if config.getvalue("trace"):
        config.pluginmanager.register(PdbTrace(), "pdbtrace")
    if config.getvalue("usepdb"):
        config.pluginmanager.register(PdbInvoke(), "pdbinvoke")

    pytestPDB._saved.append(
        (pdb.set_trace, pytestPDB._pluginmanager, pytestPDB._config)
    )
    pdb.set_trace = pytestPDB.set_trace
    pytestPDB._pluginmanager = config.pluginmanager
    pytestPDB._config = config

    # NOTE: not using pytest_unconfigure, since it might get called although
    #       pytest_configure was not (if another plugin raises UsageError).
    def fin() -> None:
        (
            pdb.set_trace,
            pytestPDB._pluginmanager,
            pytestPDB._config,
        ) = pytestPDB._saved.pop()

    config.add_cleanup(fin)


def pytest_configure(config: Config) -> None:
    import faulthandler

    # at teardown we want to restore the original faulthandler fileno
    # but faulthandler has no api to return the original fileno
    # so here we stash the stderr fileno to be used at teardown
    # sys.stderr and sys.__stderr__ may be closed or patched during the session
    # so we can't rely on their values being good at that point (#11572).
    stderr_fileno = get_stderr_fileno()
    if faulthandler.is_enabled():
        config.stash[fault_handler_original_stderr_fd_key] = stderr_fileno
    config.stash[fault_handler_stderr_fd_key] = os.dup(stderr_fileno)
    faulthandler.enable(file=config.stash[fault_handler_stderr_fd_key])


def pytest_configure(config: Config) -> None:
    """Allow plugins and conftest files to perform initial configuration.

    .. note::
        This hook is incompatible with hook wrappers.

    :param config: The pytest config object.

    Use in conftest plugins
    =======================

    This hook is called for every :ref:`initial conftest <pluginorder>` file
    after command line options have been parsed. After that, the hook is called
    for other conftest files as they are registered.
    """


def pytest_configure(config: Config) -> None:
    xmlpath = config.option.xmlpath
    # Prevent opening xmllog on worker nodes (xdist).
    if xmlpath and not hasattr(config, "workerinput"):
        junit_family = config.getini("junit_family")
        config.stash[xml_key] = LogXML(
            xmlpath,
            config.option.junitprefix,
            config.getini("junit_suite_name"),
            config.getini("junit_logging"),
            config.getini("junit_duration_report"),
            junit_family,
            config.getini("junit_log_passing_tests"),
        )
        config.pluginmanager.register(config.stash[xml_key])


def pytest_configure(config: Config) -> None:
    """Installs the LegacyTmpdirPlugin if the ``tmpdir`` plugin is also installed."""
    if config.pluginmanager.has_plugin("tmpdir"):
        mp = MonkeyPatch()
        config.add_cleanup(mp.undo)
        # Create TmpdirFactory and attach it to the config object.
        #
        # This is to comply with existing plugins which expect the handler to be
        # available at pytest_configure time, but ideally should be moved entirely
        # to the tmpdir_factory session fixture.
        try:
            tmp_path_factory = config._tmp_path_factory  # type: ignore[attr-defined]
        except AttributeError:
            # tmpdir plugin is blocked.
            pass
        else:
            _tmpdirhandler = TempdirFactory(tmp_path_factory, _ispytest=True)
            mp.setattr(config, "_tmpdirhandler", _tmpdirhandler, raising=False)

        config.pluginmanager.register(LegacyTmpdirPlugin, "legacypath-tmpdir")


def pytest_configure(config: Config) -> None:
    config.pluginmanager.register(LoggingPlugin(config), "logging-plugin")


def pytest_configure(config: Config) -> None:
    if config.option.pastebin:
        config.issue_config_time_warning(PASTEBIN, 2)

    if config.option.pastebin == "all":
        tr = config.pluginmanager.getplugin("terminalreporter")
        # If no terminal reporter plugin is present, nothing we can do here;
        # this can happen when this function executes in a worker node
        # when using pytest-xdist, for example.
        if tr is not None:
            # pastebin file will be UTF-8 encoded binary file.
            config.stash[pastebinfile_key] = tempfile.TemporaryFile("w+b")
            oldwrite = tr._tw.write

            def tee_write(s, **kwargs):
                oldwrite(s, **kwargs)
                if isinstance(s, str):
                    s = s.encode("utf-8")
                config.stash[pastebinfile_key].write(s)

            tr._tw.write = tee_write


def pytest_configure(config: Config) -> None:
    if config.getvalue("lsof"):
        checker = LsofFdLeakChecker()
        if checker.matching_platform():
            config.pluginmanager.register(checker)

    config.addinivalue_line(
        "markers",
        "pytester_example_path(*path_segments): join the given path "
        "segments to `pytester_example_dir` for this test.",
    )


def pytest_configure(config: Config) -> None:
    config.addinivalue_line(
        "markers",
        "parametrize(argnames, argvalues): call a test function multiple "
        "times passing in different arguments in turn. argvalues generally "
        "needs to be a list of values if argnames specifies only one name "
        "or a list of tuples of values if argnames specifies multiple names. "
        "Example: @parametrize('arg1', [1,2]) would lead to two calls of the "
        "decorated test function, one with arg1=1 and another with arg1=2."
        "see https://docs.pytest.org/en/stable/how-to/parametrize.html for more info "
        "and examples.",
    )
    config.addinivalue_line(
        "markers",
        "usefixtures(fixturename1, fixturename2, ...): mark tests as needing "
        "all of the specified fixtures. see "
        "https://docs.pytest.org/en/stable/explanation/fixtures.html#usefixtures ",
    )


def pytest_configure(config: Config) -> None:
    if config.option.runxfail:
        # yay a hack
        import pytest

        old = pytest.xfail
        config.add_cleanup(lambda: setattr(pytest, "xfail", old))

        def nop(*args, **kwargs):
            pass

        nop.Exception = xfail.Exception  # type: ignore[attr-defined]
        setattr(pytest, "xfail", nop)

    config.addinivalue_line(
        "markers",
        "skip(reason=None): skip the given test function with an optional reason. "
        'Example: skip(reason="no way of currently testing this") skips the '
        "test.",
    )
    config.addinivalue_line(
        "markers",
        "skipif(condition, ..., *, reason=...): "
        "skip the given test function if any of the conditions evaluate to True. "
        "Example: skipif(sys.platform == 'win32') skips the test if we are on the win32 platform. "
        "See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif",
    )
    config.addinivalue_line(
        "markers",
        "xfail(condition, ..., *, reason=..., run=True, raises=None, strict=strict_xfail): "
        "mark the test function as an expected failure if any of the conditions "
        "evaluate to True. Optionally specify a reason for better reporting "
        "and run=False if you don't even want to execute the test function. "
        "If only specific exception(s) are expected, you can list them in "
        "raises, and if the test fails in other ways, it will be reported as "
        "a true failure. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-xfail",
    )


def pytest_configure(config: Config) -> None:
    # --stepwise-skip/--stepwise-reset implies stepwise.
    if config.option.stepwise_skip or config.option.stepwise_reset:
        config.option.stepwise = True
    if config.getoption("stepwise"):
        config.pluginmanager.register(StepwisePlugin(config), "stepwiseplugin")


def pytest_configure(config: Config) -> None:
    config.stash[failed_subtests_key] = defaultdict(int)


def pytest_configure(config: Config) -> None:
    reporter = TerminalReporter(config, sys.stdout)
    config.pluginmanager.register(reporter, "terminalreporter")
    if config.option.debug or config.option.traceconfig:

        def mywriter(tags, args):
            msg = " ".join(map(str, args))
            reporter.write_line("[traceconfig] " + msg)

        config.trace.root.setprocessor("pytest:config", mywriter)

    # See terminalprogress.py.
    # On Windows it's safe to load by default.
    if sys.platform == "win32":
        config.pluginmanager.import_plugin("terminalprogress")


def pytest_configure(config: Config) -> None:
    reporter: TerminalReporter | None = config.pluginmanager.get_plugin(
        "terminalreporter"
    )

    if reporter is not None and reporter.isatty() and os.environ.get("TERM") != "dumb":
        plugin = TerminalProgressPlugin(reporter)
        config.pluginmanager.register(plugin, name="terminalprogress-plugin")


def pytest_configure(config: Config) -> None:
    prev_hook = threading.excepthook
    deque: collections.deque[ThreadExceptionMeta | BaseException] = collections.deque()
    config.stash[thread_exceptions] = deque
    config.add_cleanup(functools.partial(cleanup, config=config, prev_hook=prev_hook))
    threading.excepthook = functools.partial(thread_exception_hook, append=deque.append)


def pytest_configure(config: Config) -> None:
    """Create a TempPathFactory and attach it to the config object.

    This is to comply with existing plugins which expect the handler to be
    available at pytest_configure time, but ideally should be moved entirely
    to the tmp_path_factory session fixture.
    """
    mp = MonkeyPatch()
    config.add_cleanup(mp.undo)
    _tmp_path_factory = TempPathFactory.from_config(config, _ispytest=True)
    mp.setattr(config, "_tmp_path_factory", _tmp_path_factory, raising=False)


def pytest_configure() -> None:
    """Register the TestCaseFunction class as an IReporter if twisted.trial is available."""
    if _get_twisted_version() is not TwistedVersion.NotInstalled:
        from twisted.trial.itrial import IReporter
        from zope.interface import classImplements

        classImplements(TestCaseFunction, IReporter)


def pytest_configure(config: Config) -> None:
    prev_hook = sys.unraisablehook
    deque: collections.deque[UnraisableMeta | BaseException] = collections.deque()
    config.stash[unraisable_exceptions] = deque
    config.add_cleanup(functools.partial(cleanup, config=config, prev_hook=prev_hook))
    sys.unraisablehook = functools.partial(unraisable_hook, append=deque.append)


def pytest_configure(config: Config) -> None:
    with ExitStack() as stack:
        stack.enter_context(
            catch_warnings_for_item(
                config=config,
                ihook=config.hook,
                when="config",
                item=None,
                # this disables recording because the terminalreporter has
                # finished by the time it comes to reporting logged warnings
                # from the end of config cleanup. So for now, this is only
                # useful for setting a warning filter with an 'error' action.
                record=False,
            )
        )
        config.addinivalue_line(
            "markers",
            "filterwarnings(warning): add a warning filter to the given test. "
            "see https://docs.pytest.org/en/stable/how-to/capture-warnings.html#pytest-mark-filterwarnings ",
        )
        config.add_cleanup(stack.pop_all().close)


def pytest_configure(config: Config) -> None:
    util.validate_assertion_text_diff_style(config)


def pytest_configure(config: Config) -> None:
    config.stash[old_mark_config_key] = MARK_GEN._config
    MARK_GEN._config = config

    empty_parameterset = config.getini(EMPTY_PARAMETERSET_OPTION)

    if empty_parameterset not in ("skip", "xfail", "fail_at_collect", None, ""):
        raise UsageError(
            f"{EMPTY_PARAMETERSET_OPTION!s} must be one of skip, xfail or fail_at_collect"
            f" but it is {empty_parameterset!r}"
        )


def pytest_configure(config: Any) -> None:
  del config
  flags.FLAGS.mark_as_parsed()


def pytest_configure(config):
    # config is initialized here rather than in pytest.ini so that `pytest
    # --pyargs matplotlib` (which would not find pytest.ini) works.  The only
    # entries in pytest.ini set minversion (which is checked earlier),
    # testpaths/python_files, as they are required to properly find the tests
    for key, value in [
        ("markers", "flaky: (Provided by pytest-rerunfailures.)"),
        ("markers", "timeout: (Provided by pytest-timeout.)"),
        ("markers", "backend: Set alternate Matplotlib backend temporarily."),
        ("markers", "baseline_images: Compare output against references."),
        ("markers", "pytz: Tests that require pytz to be installed."),
        ("filterwarnings", "error"),
        ("filterwarnings",
         "ignore:.*The py23 module has been deprecated:DeprecationWarning"),
        ("filterwarnings",
         r"ignore:DynamicImporter.find_spec\(\) not found; "
         r"falling back to find_module\(\):ImportWarning"),
    ]:
        config.addinivalue_line(key, value)

    matplotlib.use('agg', force=True)
    matplotlib._called_from_pytest = True
    matplotlib._init_tests()

