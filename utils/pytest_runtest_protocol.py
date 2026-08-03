import sys

def pytest_runtest_protocol(item: Item) -> Generator[None, object, object]:
    timeout = get_timeout_config_value(item.config)
    exit_on_timeout = get_exit_on_timeout_config_value(item.config)
    if timeout > 0:
        import faulthandler

        stderr = item.config.stash[fault_handler_stderr_fd_key]
        faulthandler.dump_traceback_later(timeout, file=stderr, exit=exit_on_timeout)
        try:
            return (yield)
        finally:
            faulthandler.cancel_dump_traceback_later()
    else:
        return (yield)


def pytest_runtest_protocol(item: Item, nextitem: Item | None) -> object | None:
    """Perform the runtest protocol for a single test item.

    The default runtest protocol is this (see individual hooks for full details):

    - ``pytest_runtest_logstart(nodeid, location)``

    - Setup phase:
        - ``call = pytest_runtest_setup(item)`` (wrapped in ``CallInfo(when="setup")``)
        - ``report = pytest_runtest_makereport(item, call)``
        - ``pytest_runtest_logreport(report)``
        - ``pytest_exception_interact(call, report)`` if an interactive exception occurred

    - Call phase, if the setup passed and the ``setuponly`` pytest option is not set:
        - ``call = pytest_runtest_call(item)`` (wrapped in ``CallInfo(when="call")``)
        - ``report = pytest_runtest_makereport(item, call)``
        - ``pytest_runtest_logreport(report)``
        - ``pytest_exception_interact(call, report)`` if an interactive exception occurred

    - Teardown phase:
        - ``call = pytest_runtest_teardown(item, nextitem)`` (wrapped in ``CallInfo(when="teardown")``)
        - ``report = pytest_runtest_makereport(item, call)``
        - ``pytest_runtest_logreport(report)``
        - ``pytest_exception_interact(call, report)`` if an interactive exception occurred

    - ``pytest_runtest_logfinish(nodeid, location)``

    :param item: Test item for which the runtest protocol is performed.
    :param nextitem: The scheduled-to-be-next test item (or None if this is the end my friend).

    Stops at first non-None result, see :ref:`firstresult`.
    The return value is not used, but only stops further processing.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook.
    """


def pytest_runtest_protocol(item: Item, nextitem: Item | None) -> bool:
    ihook = item.ihook
    ihook.pytest_runtest_logstart(nodeid=item.nodeid, location=item.location)
    runtestprotocol(item, nextitem=nextitem)
    ihook.pytest_runtest_logfinish(nodeid=item.nodeid, location=item.location)
    return True


def pytest_runtest_protocol(item: Item) -> Iterator[None]:
    if _get_twisted_version() is TwistedVersion.Version24:
        import twisted.python.failure as ut

        # Monkeypatch `Failure.__init__` to store the raw exception info.
        original__init__ = ut.Failure.__init__

        def store_raw_exception_info(
            self, exc_value=None, exc_type=None, exc_tb=None, captureVars=None
        ):  # pragma: no cover
            if exc_value is None:
                raw_exc_info = sys.exc_info()
            else:
                if exc_type is None:
                    exc_type = type(exc_value)
                if exc_tb is None:
                    exc_tb = sys.exc_info()[2]
                raw_exc_info = (exc_type, exc_value, exc_tb)
            setattr(self, TWISTED_RAW_EXCINFO_ATTR, tuple(raw_exc_info))
            try:
                original__init__(
                    self, exc_value, exc_type, exc_tb, captureVars=captureVars
                )
            except TypeError:  # pragma: no cover
                original__init__(self, exc_value, exc_type, exc_tb)

        with MonkeyPatch.context() as patcher:
            patcher.setattr(ut.Failure, "__init__", store_raw_exception_info)
            return (yield)
    else:
        return (yield)


def pytest_runtest_protocol(item: Item) -> Generator[None, object, object]:
    with catch_warnings_for_item(
        config=item.config, ihook=item.ihook, when="runtest", item=item
    ):
        return (yield)


def pytest_runtest_protocol(item: Item) -> Generator[None, object, object]:
    """Setup the pytest_assertrepr_compare and pytest_assertion_pass hooks.

    The rewrite module will use util._reprcompare if it exists to use custom
    reporting via the pytest_assertrepr_compare hook.  This sets up this custom
    comparison for the test.
    """
    ihook = item.ihook

    def callbinrepr(op, left: object, right: object) -> str | None:
        """Call the pytest_assertrepr_compare hook and prepare the result.

        This uses the first result from the hook and then ensures the
        following:
        * Overly verbose explanations are truncated unless configured otherwise
          (eg. if running in verbose mode).
        * Embedded newlines are escaped to help util.format_explanation()
          later.
        * If the rewrite mode is used embedded %-characters are replaced
          to protect later % formatting.

        The result can be formatted by util.format_explanation() for
        pretty printing.
        """
        hook_result = ihook.pytest_assertrepr_compare(
            config=item.config, op=op, left=left, right=right
        )
        for new_expl in hook_result:
            if new_expl:
                new_expl = truncate.truncate_if_required(new_expl, item)
                new_expl = [line.replace("\n", "\\n") for line in new_expl]
                res = "\n~".join(new_expl)
                if item.config.getvalue("assertmode") == "rewrite":
                    res = res.replace("%", "%%")
                return res
        return None

    saved_assert_hooks = util._reprcompare, util._assertion_pass
    util._reprcompare = callbinrepr
    util._config = item.config

    if ihook.pytest_assertion_pass.get_hookimpls():

        def call_assertion_pass_hook(lineno: int, orig: str, expl: str) -> None:
            ihook.pytest_assertion_pass(item=item, lineno=lineno, orig=orig, expl=expl)

        util._assertion_pass = call_assertion_pass_hook

    try:
        return (yield)
    finally:
        util._reprcompare, util._assertion_pass = saved_assert_hooks
        util._config = None

