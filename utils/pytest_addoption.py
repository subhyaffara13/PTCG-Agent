
def pytest_addoption(parser):  # type: ignore[no-untyped-def]
    parser.addoption(
        "--aiohttp-fast",
        action="store_true",
        default=False,
        help="run tests faster by disabling extra checks",
    )
    parser.addoption(
        "--aiohttp-loop",
        action="store",
        default="pyloop",
        help="run tests with specific loop: pyloop, uvloop or all",
    )
    parser.addoption(
        "--aiohttp-enable-loop-debug",
        action="store_true",
        default=False,
        help="enable event loop debug mode",
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addini(
        "anyio_mode",
        default="strict",
        help='AnyIO plugin mode (either "strict" or "auto")',
    )


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--backend",
        action="store",
        default=None,
        help="Run tests with a backend by auto-converting nx graphs to backend graphs",
    )
    parser.addoption(
        "--fallback-to-nx",
        action="store_true",
        default=False,
        help="Run nx function if a backend doesn't implement a dispatchable function"
        " (use with --backend)",
    )


def pytest_addoption(parser):
    parser.addoption("--available-memory", action="store", default=None,
                     help=("Set amount of memory available for running the "
                           "test suite. This can result to tests requiring "
                           "especially large amounts of memory to be skipped. "
                           "Equivalent to setting environment variable "
                           "NPY_AVAILABLE_MEM. Default: determined"
                           "automatically."))


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--no-strict-data-files",
        action="store_false",
        help="Don't fail if a test is skipped for missing data file.",
    )


def pytest_addoption(parser):
    parser.addoption("--split", action="store", default="", help="split tests")


def pytest_addoption(parser: Parser) -> None:
    """Add command-line options for cache functionality.

    :param parser: Parser object to add command-line options to.
    """
    group = parser.getgroup("general")
    group.addoption(
        "--lf",
        "--last-failed",
        action="store_true",
        dest="lf",
        help="Rerun only the tests that failed at the last run (or all if none failed)",
    )
    group.addoption(
        "--ff",
        "--failed-first",
        action="store_true",
        dest="failedfirst",
        help="Run all tests, but run the last failures first. "
        "This may re-order tests and thus lead to "
        "repeated fixture setup/teardown.",
    )
    group.addoption(
        "--nf",
        "--new-first",
        action="store_true",
        dest="newfirst",
        help="Run tests from new files first, then the rest of the tests "
        "sorted by file mtime",
    )
    group.addoption(
        "--cache-show",
        action="append",
        nargs="?",
        dest="cacheshow",
        help=(
            "Show cache contents, don't perform collection or tests. "
            "Optional argument: glob (default: '*')."
        ),
    )
    group.addoption(
        "--cache-clear",
        action="store_true",
        dest="cacheclear",
        help="Remove all cache contents at start of test run",
    )
    cache_dir_default = ".pytest_cache"
    if "TOX_ENV_DIR" in os.environ:
        cache_dir_default = os.path.join(os.environ["TOX_ENV_DIR"], cache_dir_default)
    parser.addini("cache_dir", default=cache_dir_default, help="Cache directory path")
    group.addoption(
        "--lfnf",
        "--last-failed-no-failures",
        action="store",
        dest="last_failed_no_failures",
        choices=("all", "none"),
        default="all",
        help="With ``--lf``, determines whether to execute tests when there "
        "are no previously (known) failures or when no "
        "cached ``lastfailed`` data was found. "
        "``all`` (the default) runs the full test suite again. "
        "``none`` just emits a message about no known failures and exits successfully.",
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("general")
    group.addoption(
        "--capture",
        action="store",
        default="fd",
        metavar="method",
        choices=["fd", "sys", "no", "tee-sys"],
        help="Per-test capturing method: one of fd|sys|no|tee-sys",
    )
    group._addoption(  # private to use reserved lower-case short option
        "-s",
        action="store_const",
        const="no",
        dest="capture",
        help="Shortcut for --capture=no",
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("general")
    group.addoption(
        "--pdb",
        dest="usepdb",
        action="store_true",
        help="Start the interactive Python debugger on errors or KeyboardInterrupt",
    )
    group.addoption(
        "--pdbcls",
        dest="usepdb_cls",
        metavar="modulename:classname",
        type=_validate_usepdb_cls,
        help="Specify a custom interactive Python debugger for use with --pdb."
        "For example: --pdbcls=IPython.terminal.debugger:TerminalPdb",
    )
    group.addoption(
        "--trace",
        dest="trace",
        action="store_true",
        help="Immediately break when running each test",
    )


def pytest_addoption(parser: Parser) -> None:
    parser.addini(
        "doctest_optionflags",
        "Option flags for doctests",
        type="args",
        default=["ELLIPSIS"],
    )
    parser.addini(
        "doctest_encoding", "Encoding used for doctest files", default="utf-8"
    )
    group = parser.getgroup("collect")
    group.addoption(
        "--doctest-modules",
        action="store_true",
        default=False,
        help="Run doctests in all .py modules",
        dest="doctestmodules",
    )
    group.addoption(
        "--doctest-report",
        type=str.lower,
        default="udiff",
        help="Choose another output format for diffs on doctest failure",
        choices=DOCTEST_REPORT_CHOICES,
        dest="doctestreport",
    )
    group.addoption(
        "--doctest-glob",
        action="append",
        default=[],
        metavar="pat",
        help="Doctests file matching pattern, default: test*.txt",
        dest="doctestglob",
    )
    group.addoption(
        "--doctest-ignore-import-errors",
        action="store_true",
        default=False,
        help="Ignore doctest collection errors",
        dest="doctest_ignore_import_errors",
    )
    group.addoption(
        "--doctest-continue-on-failure",
        action="store_true",
        default=False,
        help="For a given doctest, continue to run after the first failure",
        dest="doctest_continue_on_failure",
    )


def pytest_addoption(parser: Parser) -> None:
    help_timeout = (
        "Dump the traceback of all threads if a test takes "
        "more than TIMEOUT seconds to finish"
    )
    help_exit_on_timeout = (
        "Exit the test process if a test takes more than "
        "faulthandler_timeout seconds to finish"
    )
    parser.addini("faulthandler_timeout", help_timeout, default=0.0)
    parser.addini(
        "faulthandler_exit_on_timeout", help_exit_on_timeout, type="bool", default=False
    )


def pytest_addoption(parser: Parser) -> None:
    parser.addini(
        "usefixtures",
        type="args",
        default=[],
        help="List of default fixtures to be used with this project",
    )
    group = parser.getgroup("general")
    group.addoption(
        "--fixtures",
        "--funcargs",
        action="store_true",
        dest="showfixtures",
        default=False,
        help="Show available fixtures, sorted by plugin appearance "
        "(fixtures with leading '_' are only shown with '-v')",
    )
    group.addoption(
        "--fixtures-per-test",
        action="store_true",
        dest="show_fixtures_per_test",
        default=False,
        help="Show fixtures per test",
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("debugconfig")
    group.addoption(
        "-V",
        "--version",
        action="count",
        default=0,
        dest="version",
        help="Display pytest version and information about plugins. "
        "When given twice, also display information about plugins.",
    )
    group._addoption(  # private to use reserved lower-case short option
        "-h",
        "--help",
        action=HelpAction,
        dest="help",
        help="Show help message and configuration info",
    )
    group._addoption(  # private to use reserved lower-case short option
        "-p",
        action="append",
        dest="plugins",
        default=[],
        metavar="name",
        help="Early-load given plugin module name or entry point (multi-allowed). "
        "To avoid loading of plugins, use the `no:` prefix, e.g. "
        "`no:doctest`. See also --disable-plugin-autoload.",
    )
    group.addoption(
        "--disable-plugin-autoload",
        action="store_true",
        default=False,
        help="Disable plugin auto-loading through entry point packaging metadata. "
        "Only plugins explicitly specified in -p or env var PYTEST_PLUGINS will be loaded.",
    )
    group.addoption(
        "--traceconfig",
        "--trace-config",
        action="store_true",
        default=False,
        help="Trace considerations of conftest.py files",
    )
    group.addoption(
        "--debug",
        action="store",
        nargs="?",
        const="pytestdebug.log",
        dest="debug",
        metavar="DEBUG_FILE_NAME",
        help="Store internal tracing debug information in this log file. "
        "This file is opened with 'w' and truncated as a result, care advised. "
        "Default: pytestdebug.log.",
    )
    group._addoption(  # private to use reserved lower-case short option
        "-o",
        "--override-ini",
        dest="override_ini",
        action="append",
        help='Override configuration option with "option=value" style, '
        "e.g. `-o strict_xfail=True -o cache_dir=cache`.",
    )


def pytest_addoption(parser: Parser, pluginmanager: PytestPluginManager) -> None:
    """Register argparse-style options and config-style config values,
    called once at the beginning of a test run.

    :param parser:
        To add command line options, call
        :py:func:`parser.addoption(...) <pytest.Parser.addoption>`.
        To add config-file values call :py:func:`parser.addini(...)
        <pytest.Parser.addini>`.

    :param pluginmanager:
        The pytest plugin manager, which can be used to install :py:func:`~pytest.hookspec`'s
        or :py:func:`~pytest.hookimpl`'s and allow one plugin to call another plugin's hooks
        to change how command line options are added.

    Options can later be accessed through the
    :py:class:`config <pytest.Config>` object, respectively:

    - :py:func:`config.getoption(name) <pytest.Config.getoption>` to
      retrieve the value of a command line option.

    - :py:func:`config.getini(name) <pytest.Config.getini>` to retrieve
      a value read from a configuration file.

    The config object is passed around on many internal objects via the ``.config``
    attribute or can be retrieved as the ``pytestconfig`` fixture.

    .. note::
        This hook is incompatible with hook wrappers.

    Use in conftest plugins
    =======================

    If a conftest plugin implements this hook, it will be called immediately
    when the conftest is registered.

    This hook is only called for :ref:`initial conftests <pluginorder>`.
    """


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--junitxml",
        "--junit-xml",
        action="store",
        dest="xmlpath",
        metavar="path",
        type=functools.partial(filename_arg, optname="--junitxml"),
        default=None,
        help="Create junit-xml style report file at given path",
    )
    group.addoption(
        "--junitprefix",
        "--junit-prefix",
        action="store",
        metavar="str",
        default=None,
        help="Prepend prefix to classnames in junit-xml output",
    )
    parser.addini(
        "junit_suite_name", "Test suite name for JUnit report", default="pytest"
    )
    parser.addini(
        "junit_logging",
        "Write captured log messages to JUnit report: "
        "one of no|log|system-out|system-err|out-err|all",
        default="no",
    )
    parser.addini(
        "junit_log_passing_tests",
        "Capture log information for passing tests to JUnit report: ",
        type="bool",
        default=True,
    )
    parser.addini(
        "junit_duration_report",
        "Duration time to report: one of total|call",
        default="total",
    )  # choices=['total', 'call'])
    parser.addini(
        "junit_family",
        "Emit XML for schema: one of legacy|xunit1|xunit2",
        default="xunit2",
    )


def pytest_addoption(parser: Parser) -> None:
    """Add options to control log capturing."""
    group = parser.getgroup("logging")

    def add_option_ini(option, dest, default=None, type=None, **kwargs):
        parser.addini(
            dest, default=default, type=type, help="Default value for " + option
        )
        group.addoption(option, dest=dest, **kwargs)

    add_option_ini(
        "--log-level",
        dest="log_level",
        default=None,
        metavar="LEVEL",
        help=(
            "Level of messages to catch/display."
            " Not set by default, so it depends on the root/parent log handler's"
            ' effective level, where it is "WARNING" by default.'
        ),
    )
    add_option_ini(
        "--log-format",
        dest="log_format",
        default=DEFAULT_LOG_FORMAT,
        help="Log format used by the logging module",
    )
    add_option_ini(
        "--log-date-format",
        dest="log_date_format",
        default=DEFAULT_LOG_DATE_FORMAT,
        help="Log date format used by the logging module",
    )
    parser.addini(
        "log_cli",
        default=False,
        type="bool",
        help='Enable log display during test run (also known as "live logging")',
    )
    add_option_ini(
        "--log-cli-level", dest="log_cli_level", default=None, help="CLI logging level"
    )
    add_option_ini(
        "--log-cli-format",
        dest="log_cli_format",
        default=None,
        help="Log format used by the logging module",
    )
    add_option_ini(
        "--log-cli-date-format",
        dest="log_cli_date_format",
        default=None,
        help="Log date format used by the logging module",
    )
    add_option_ini(
        "--log-file",
        dest="log_file",
        default=None,
        help="Path to a file when logging will be written to",
    )
    add_option_ini(
        "--log-file-mode",
        dest="log_file_mode",
        default="w",
        choices=["w", "a"],
        help="Log file open mode",
    )
    add_option_ini(
        "--log-file-level",
        dest="log_file_level",
        default=None,
        help="Log file logging level",
    )
    add_option_ini(
        "--log-file-format",
        dest="log_file_format",
        default=None,
        help="Log format used by the logging module",
    )
    add_option_ini(
        "--log-file-date-format",
        dest="log_file_date_format",
        default=None,
        help="Log date format used by the logging module",
    )
    add_option_ini(
        "--log-auto-indent",
        dest="log_auto_indent",
        default=None,
        help="Auto-indent multiline messages passed to the logging module. Accepts true|on, false|off or an integer.",
    )
    group.addoption(
        "--log-disable",
        action="append",
        default=[],
        dest="logger_disable",
        help="Disable a logger by name. Can be passed multiple times.",
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("general")
    group._addoption(  # private to use reserved lower-case short option
        "-x",
        "--exitfirst",
        action="store_const",
        dest="maxfail",
        const=1,
        help="Exit instantly on first error or failed test",
    )
    group.addoption(
        "--maxfail",
        metavar="num",
        action="store",
        type=int,
        dest="maxfail",
        default=0,
        help="Exit after first num failures or errors",
    )
    group.addoption(
        "--strict-config",
        action=OverrideIniAction,
        ini_option="strict_config",
        ini_value="true",
        help="Enables the strict_config option",
    )
    group.addoption(
        "--strict-markers",
        action=OverrideIniAction,
        ini_option="strict_markers",
        ini_value="true",
        help="Enables the strict_markers option",
    )
    group.addoption(
        "--strict",
        action=OverrideIniAction,
        ini_option="strict",
        ini_value="true",
        help="Enables the strict option",
    )
    parser.addini(
        "strict_config",
        "Any warnings encountered while parsing the `pytest` section of the "
        "configuration file raise errors",
        type="bool",
        # None => fallback to `strict`.
        default=None,
    )
    parser.addini(
        "strict_markers",
        "Markers not registered in the `markers` section of the configuration "
        "file raise errors",
        type="bool",
        # None => fallback to `strict`.
        default=None,
    )
    parser.addini(
        "strict",
        "Enables all strictness options, currently: "
        "strict_config, strict_markers, strict_xfail, strict_parametrization_ids",
        type="bool",
        default=False,
    )

    group = parser.getgroup("pytest-warnings")
    group.addoption(
        "-W",
        "--pythonwarnings",
        action="append",
        help="Set which warnings to report, see -W option of Python itself",
    )
    group.addoption(
        "--max-warnings",
        action="store",
        type=int,
        default=None,
        metavar="num",
        dest="max_warnings",
        help="Exit with error if all tests pass but the number of warnings exceeds this threshold",
    )
    parser.addini(
        "filterwarnings",
        type="linelist",
        help="Each line specifies a pattern for "
        "warnings.filterwarnings. "
        "Processed after -W/--pythonwarnings.",
    )
    parser.addini(
        "max_warnings",
        help="Exit with error if all tests pass but the number of warnings exceeds this threshold",
    )

    group = parser.getgroup("collect", "collection")
    group.addoption(
        "--collectonly",
        "--collect-only",
        "--co",
        action="store_true",
        help="Only collect tests, don't execute them",
    )
    group.addoption(
        "--pyargs",
        action="store_true",
        help="Try to interpret all arguments as Python packages",
    )
    group.addoption(
        "--ignore",
        action="append",
        metavar="path",
        help="Ignore path during collection (multi-allowed)",
    )
    group.addoption(
        "--ignore-glob",
        action="append",
        metavar="path",
        help="Ignore path pattern during collection (multi-allowed)",
    )
    group.addoption(
        "--deselect",
        action="append",
        metavar="nodeid_prefix",
        help="Deselect item (via node id prefix) during collection (multi-allowed)",
    )
    group.addoption(
        "--confcutdir",
        dest="confcutdir",
        default=None,
        metavar="dir",
        type=functools.partial(directory_arg, optname="--confcutdir"),
        help="Only load conftest.py's relative to specified dir",
    )
    group.addoption(
        "--noconftest",
        action="store_true",
        dest="noconftest",
        default=False,
        help="Don't load any conftest.py files",
    )
    group.addoption(
        "--keepduplicates",
        "--keep-duplicates",
        action="store_true",
        dest="keepduplicates",
        default=False,
        help="Keep duplicate tests",
    )
    group.addoption(
        "--collect-in-virtualenv",
        action="store_true",
        dest="collect_in_virtualenv",
        default=False,
        help="Don't ignore tests in a local virtualenv directory",
    )
    group.addoption(
        "--continue-on-collection-errors",
        action="store_true",
        default=False,
        dest="continue_on_collection_errors",
        help="Force test execution even if collection errors occur",
    )
    group.addoption(
        "--import-mode",
        default="prepend",
        choices=["prepend", "append", "importlib"],
        dest="importmode",
        help="Prepend/append to sys.path when importing test modules and conftest "
        "files. Default: prepend.",
    )
    parser.addini(
        "norecursedirs",
        "Directory patterns to avoid for recursion",
        type="args",
        default=[
            "*.egg",
            ".*",
            "_darcs",
            "build",
            "CVS",
            "dist",
            "node_modules",
            "venv",
            "{arch}",
        ],
    )
    parser.addini(
        "testpaths",
        "Directories to search for tests when no files or directories are given on the "
        "command line",
        type="args",
        default=[],
    )
    parser.addini(
        "collect_imported_tests",
        "Whether to collect tests in imported modules outside `testpaths`",
        type="bool",
        default=True,
    )
    parser.addini(
        "consider_namespace_packages",
        type="bool",
        default=False,
        help="Consider namespace packages when resolving module names during import",
    )

    group = parser.getgroup("debugconfig", "test session debugging and configuration")
    group._addoption(  # private to use reserved lower-case short option
        "-c",
        "--config-file",
        metavar="FILE",
        type=str,
        dest="inifilename",
        help="Load configuration from `FILE` instead of trying to locate one of the "
        "implicit configuration files.",
    )
    group.addoption(
        "--rootdir",
        action="store",
        dest="rootdir",
        help="Define root directory for tests. Can be relative path: 'root_dir', './root_dir', "
        "'root_dir/another_dir/'; absolute path: '/home/user/root_dir'; path with variables: "
        "'$HOME/root_dir'.",
    )
    group.addoption(
        "--basetemp",
        dest="basetemp",
        default=None,
        type=validate_basetemp,
        metavar="dir",
        help=(
            "Base temporary directory for this test run. "
            "(Warning: this directory is removed if it exists.)"
        ),
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--pastebin",
        metavar="mode",
        action="store",
        dest="pastebin",
        default=None,
        choices=["failed", "all"],
        help="Send failed|all info to bpaste.net pastebin service",
    )


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--lsof",
        action="store_true",
        dest="lsof",
        default=False,
        help="Run FD checks if lsof is available",
    )

    parser.addoption(
        "--runpytest",
        default="inprocess",
        dest="runpytest",
        choices=("inprocess", "subprocess"),
        help=(
            "Run pytest sub runs in tests using an 'inprocess' "
            "or 'subprocess' (python -m main) method"
        ),
    )

    parser.addini(
        "pytester_example_dir", help="Directory to take the pytester example files from"
    )


def pytest_addoption(parser: Parser) -> None:
    parser.addini(
        "python_files",
        type="args",
        # NOTE: default is also used in AssertionRewritingHook.
        default=["test_*.py", "*_test.py"],
        help="Glob-style file patterns for Python test module discovery",
    )
    parser.addini(
        "python_classes",
        type="args",
        default=["Test"],
        help="Prefixes or glob names for Python test class discovery",
    )
    parser.addini(
        "python_functions",
        type="args",
        default=["test"],
        help="Prefixes or glob names for Python test function and method discovery",
    )
    parser.addini(
        "disable_test_id_escaping_and_forfeit_all_rights_to_community_support",
        type="bool",
        default=False,
        help="Disable string escape non-ASCII characters, might cause unwanted "
        "side effects(use at your own risk)",
    )
    parser.addini(
        "strict_parametrization_ids",
        type="bool",
        # None => fallback to `strict`.
        default=None,
        help="Emit an error if non-unique parameter set IDs are detected",
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("terminal reporting", "Reporting", after="general")
    group.addoption(
        "--durations",
        action="store",
        type=int,
        default=None,
        metavar="N",
        help="Show N slowest setup/test durations (N=0 for all)",
    )
    group.addoption(
        "--durations-min",
        action="store",
        type=float,
        default=None,
        metavar="N",
        help="Minimal duration in seconds for inclusion in slowest list. "
        "Default: 0.005 (or 0.0 if -vv is given).",
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("debugconfig")
    group.addoption(
        "--setuponly",
        "--setup-only",
        action="store_true",
        help="Only setup fixtures, do not execute tests",
    )
    group.addoption(
        "--setupshow",
        "--setup-show",
        action="store_true",
        help="Show setup of fixtures while executing tests",
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("debugconfig")
    group.addoption(
        "--setupplan",
        "--setup-plan",
        action="store_true",
        help="Show what fixtures and tests would be executed but "
        "don't execute anything",
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("general")
    group.addoption(
        "--runxfail",
        action="store_true",
        dest="runxfail",
        default=False,
        help="Report the results of xfail tests as if they were not marked",
    )

    parser.addini(
        "strict_xfail",
        "Default for the strict parameter of xfail "
        "markers when not given explicitly (default: False) (alias: xfail_strict)",
        type="bool",
        # None => fallback to `strict`.
        default=None,
        aliases=["xfail_strict"],
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("general")
    group.addoption(
        "--sw",
        "--stepwise",
        action="store_true",
        default=False,
        dest="stepwise",
        help="Exit on test failure and continue from last failing test next time",
    )
    group.addoption(
        "--sw-skip",
        "--stepwise-skip",
        action="store_true",
        default=False,
        dest="stepwise_skip",
        help="Ignore the first failing test but stop on the next failing test. "
        "Implicitly enables --stepwise.",
    )
    group.addoption(
        "--sw-reset",
        "--stepwise-reset",
        action="store_true",
        default=False,
        dest="stepwise_reset",
        help="Resets stepwise state, restarting the stepwise workflow. "
        "Implicitly enables --stepwise.",
    )


def pytest_addoption(parser: Parser) -> None:
    Config._add_verbosity_ini(
        parser,
        Config.VERBOSITY_SUBTESTS,
        help=(
            "Specify verbosity level for subtests. "
            "Higher levels will generate output for passed subtests. Failed subtests are always reported."
        ),
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("terminal reporting", "Reporting", after="general")
    group._addoption(  # private to use reserved lower-case short option
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbose",
        help="Increase verbosity",
    )
    group.addoption(
        "--no-header",
        action="store_true",
        default=False,
        dest="no_header",
        help="Disable header",
    )
    group.addoption(
        "--no-summary",
        action="store_true",
        default=False,
        dest="no_summary",
        help="Disable summary",
    )
    group.addoption(
        "--no-fold-skipped",
        action="store_false",
        dest="fold_skipped",
        default=True,
        help="Do not fold skipped tests in short summary.",
    )
    group.addoption(
        "--force-short-summary",
        action="store_true",
        dest="force_short_summary",
        default=False,
        help="Force condensed summary output regardless of verbosity level.",
    )
    group._addoption(  # private to use reserved lower-case short option
        "-q",
        "--quiet",
        action=MoreQuietAction,
        default=0,
        dest="verbose",
        help="Decrease verbosity",
    )
    group.addoption(
        "--verbosity",
        dest="verbose",
        type=int,
        default=0,
        help="Set verbosity. Default: 0.",
    )
    group._addoption(  # private to use reserved lower-case short option
        "-r",
        "--report-chars",
        action="store",
        dest="reportchars",
        default=_REPORTCHARS_DEFAULT,
        metavar="chars",
        help="Show extra test summary info as specified by chars: (f)ailed, "
        "(E)rror, (s)kipped, (x)failed, (X)passed, "
        "(p)assed, (P)assed with output, (a)ll except passed (p/P), or (A)ll. "
        "(w)arnings are enabled by default (see --disable-warnings), "
        "'N' can be used to reset the list. (default: 'fE').",
    )
    group.addoption(
        "--disable-warnings",
        "--disable-pytest-warnings",
        default=False,
        dest="disable_warnings",
        action="store_true",
        help="Disable warnings summary",
    )
    group._addoption(  # private to use reserved lower-case short option
        "-l",
        "--showlocals",
        action="store_true",
        dest="showlocals",
        default=False,
        help="Show locals in tracebacks (disabled by default)",
    )
    group.addoption(
        "--no-showlocals",
        action="store_false",
        dest="showlocals",
        help="Hide locals in tracebacks (negate --showlocals passed through addopts)",
    )
    group.addoption(
        "--tb",
        metavar="style",
        action="store",
        dest="tbstyle",
        default="auto",
        choices=["auto", "long", "short", "no", "line", "native"],
        help="Traceback print mode (auto/long/short/line/native/no)",
    )
    group.addoption(
        "--xfail-tb",
        action="store_true",
        dest="xfail_tb",
        default=False,
        help="Show tracebacks for xfail (as long as --tb != no)",
    )
    group.addoption(
        "--show-capture",
        action="store",
        dest="showcapture",
        choices=["no", "stdout", "stderr", "log", "all"],
        default="all",
        help="Controls how captured stdout/stderr/log is shown on failed tests. "
        "Default: all.",
    )
    group.addoption(
        "--fulltrace",
        "--full-trace",
        action="store_true",
        default=False,
        help="Don't cut any tracebacks (default is to cut)",
    )
    group.addoption(
        "--color",
        metavar="color",
        action="store",
        dest="color",
        default="auto",
        choices=["yes", "no", "auto"],
        help="Color terminal output (yes/no/auto)",
    )
    group.addoption(
        "--code-highlight",
        default="yes",
        choices=["yes", "no"],
        help="Whether code should be highlighted (only if --color is also enabled). "
        "Default: yes.",
    )

    parser.addini(
        "console_output_style",
        help='Console output: "classic", or with additional progress information '
        '("progress" (percentage) | "count" | "progress-even-when-capture-no" (forces '
        "progress even when capture=no)",
        default="progress",
    )
    Config._add_verbosity_ini(
        parser,
        Config.VERBOSITY_TEST_CASES,
        help=(
            "Specify a verbosity level for test case execution, overriding the main level. "
            "Higher levels will provide more detailed information about each test case executed."
        ),
    )


def pytest_addoption(parser: Parser) -> None:
    parser.addini(
        "tmp_path_retention_count",
        help="How many sessions should we keep the `tmp_path` directories, according to `tmp_path_retention_policy`.",
        default="3",
        # NOTE: Would have been better as an `int` but can't change it now.
        type="string",
    )

    parser.addini(
        "tmp_path_retention_policy",
        help="Controls which directories created by the `tmp_path` fixture are kept around, based on test outcome. "
        "(all/failed/none)",
        type="string",
        default="all",
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("debugconfig")
    group.addoption(
        "--assert",
        action="store",
        dest="assertmode",
        choices=("rewrite", "plain"),
        default="rewrite",
        metavar="MODE",
        help=(
            "Control assertion debugging tools.\n"
            "'plain' performs no assertion debugging.\n"
            "'rewrite' (the default) rewrites assert statements in test modules"
            " on import to provide assert expression information."
        ),
    )
    parser.addini(
        "enable_assertion_pass_hook",
        type="bool",
        default=False,
        help="Enables the pytest_assertion_pass hook. "
        "Make sure to delete any previously generated pyc cache files.",
    )

    parser.addini(
        "truncation_limit_lines",
        default=None,
        help="Set threshold of LINES after which truncation will take effect",
    )
    parser.addini(
        "truncation_limit_chars",
        default=None,
        help=("Set threshold of CHARS after which truncation will take effect"),
    )
    parser.addini(
        "assertion_text_diff_style",
        default=util.ASSERTION_TEXT_DIFF_STYLE_NDIFF,
        help=(
            "Choose how pytest renders diffs for string equality assertions: "
            f"{util.ASSERTION_TEXT_DIFF_STYLE_NDIFF} or "
            f"{util.ASSERTION_TEXT_DIFF_STYLE_BLOCK}"
        ),
    )

    Config._add_verbosity_ini(
        parser,
        Config.VERBOSITY_ASSERTIONS,
        help=(
            "Specify a verbosity level for assertions, overriding the main level. "
            "Higher levels will provide more detailed explanation when an assertion fails."
        ),
    )


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("general")
    group._addoption(  # private to use reserved lower-case short option
        "-k",
        action="store",
        dest="keyword",
        default="",
        metavar="EXPRESSION",
        help="Only run tests which match the given substring expression. "
        "An expression is a Python evaluable expression "
        "where all names are substring-matched against test names "
        "and their parent classes. Example: -k 'test_method or test_"
        "other' matches all test functions and classes whose name "
        "contains 'test_method' or 'test_other', while -k 'not test_method' "
        "matches those that don't contain 'test_method' in their names. "
        "-k 'not test_method and not test_other' will eliminate the matches. "
        "Additionally keywords are matched to classes and functions "
        "containing extra names in their 'extra_keyword_matches' set, "
        "as well as functions which have names assigned directly to them. "
        "The matching is case-insensitive.",
    )

    group._addoption(  # private to use reserved lower-case short option
        "-m",
        action="store",
        dest="markexpr",
        default="",
        metavar="MARKEXPR",
        help="Only run tests matching given mark expression. "
        "For example: -m 'mark1 and not mark2'.",
    )

    group.addoption(
        "--markers",
        action="store_true",
        help="show markers (builtin, plugin and per-project ones).",
    )

    parser.addini("markers", "Register new markers for test functions", "linelist")
    parser.addini(EMPTY_PARAMETERSET_OPTION, "Default marker for empty parametersets")


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("mypy")
    group.addoption(
        "--update-data",
        action="store_true",
        default=False,
        help="Update test data to reflect actual output (supported only for certain tests)",
    )
    group.addoption(
        "--mypy-num-workers",
        type=int,
        default=0,
        help="Run tests using multiple worker processes for each test case",
    )
    group.addoption(
        "--save-failures-to",
        default=None,
        help="Copy the temp directories from failing tests to a target directory",
    )
    group.addoption(
        "--mypy-verbose", action="count", help="Set the verbose flag when creating mypy Options"
    )
    group.addoption(
        "--mypyc-showc",
        action="store_true",
        default=False,
        help="Display C code on mypyc test failures",
    )
    group.addoption(
        "--mypyc-debug",
        default=None,
        dest="debugger",
        choices=SUPPORTED_DEBUGGERS,
        help="Run the first mypyc run test with the specified debugger",
    )

