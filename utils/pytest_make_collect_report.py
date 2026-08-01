
def pytest_make_collect_report(collector: Collector) -> CollectReport | None:
    """Perform :func:`collector.collect() <pytest.Collector.collect>` and return
    a :class:`~pytest.CollectReport`.

    Stops at first non-None result, see :ref:`firstresult`.

    :param collector:
        The collector.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given collector, only
    conftest files in the collector's directory and its parent directories are
    consulted.
    """


def pytest_make_collect_report(collector: Collector) -> CollectReport:
    def collect() -> list[Item | Collector]:
        # Before collecting, if this is a Directory, load the conftests.
        # If a conftest import fails to load, it is considered a collection
        # error of the Directory collector. This is why it's done inside of the
        # CallInfo wrapper.
        #
        # Note: initial conftests are loaded early, not here.
        if isinstance(collector, Directory):
            collector.config.pluginmanager._loadconftestmodules(
                collector.path,
                collector.config.getoption("importmode"),
                rootpath=collector.config.rootpath,
                consider_namespace_packages=collector.config.getini(
                    "consider_namespace_packages"
                ),
            )

        return list(collector.collect())

    call = CallInfo.from_call(
        collect, "collect", reraise=(KeyboardInterrupt, SystemExit)
    )
    longrepr: None | tuple[str, int, str] | str | TerminalRepr = None
    if not call.excinfo:
        outcome: Literal["passed", "skipped", "failed"] = "passed"
    else:
        skip_exceptions = [Skipped]
        unittest = sys.modules.get("unittest")
        if unittest is not None:
            skip_exceptions.append(unittest.SkipTest)
        if isinstance(call.excinfo.value, tuple(skip_exceptions)):
            outcome = "skipped"
            r_ = collector._repr_failure_py(call.excinfo, "line")
            assert isinstance(r_, ExceptionChainRepr), repr(r_)
            r = r_.reprcrash
            assert r
            longrepr = (str(r.path), r.lineno, r.message)
        else:
            outcome = "failed"
            errorinfo = collector.repr_failure(call.excinfo)
            if not hasattr(errorinfo, "toterminal"):
                assert isinstance(errorinfo, str)
                errorinfo = CollectErrorRepr(errorinfo)
            longrepr = errorinfo
    result = call.result if not call.excinfo else None
    rep = CollectReport(collector.nodeid, outcome, longrepr, result)
    rep.call = call  # type: ignore # see collect_one_node
    return rep

