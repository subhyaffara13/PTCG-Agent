import sys

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if NOGIL_BUILD and not gil_enabled_at_start and sys._is_gil_enabled():
        tr = terminalreporter
        tr.ensure_newline()
        tr.section("GIL re-enabled", sep="=", red=True, bold=True)
        tr.line("The GIL was re-enabled at runtime during the tests.")
        tr.line("This can happen with no test failures if the RuntimeWarning")
        tr.line("raised by Python when this happens is filtered by a test.")
        tr.line("")
        tr.line("Please ensure all new C modules declare support for running")
        tr.line("without the GIL. Any new tests that intentionally imports ")
        tr.line("code that re-enables the GIL should do so in a subprocess.")
        pytest.exit("GIL re-enabled during tests", returncode=1)


def pytest_terminal_summary(terminalreporter):
    if terminalreporter.stats.get("error", None) or terminalreporter.stats.get(
        "failed", None
    ):
        terminalreporter.write_sep(" ", "DO *NOT* COMMIT!", red=True, bold=True)


def pytest_terminal_summary(
    terminalreporter: TerminalReporter,
    exitstatus: ExitCode,
    config: Config,
) -> None:
    """Add a section to terminal summary reporting.

    :param terminalreporter: The internal terminal reporter object.
    :param exitstatus: The exit status that will be reported back to the OS.
    :param config: The pytest config object.

    .. versionadded:: 4.2
        The ``config`` parameter.

    Use in conftest plugins
    =======================

    Any conftest plugin can implement this hook.
    """


def pytest_terminal_summary(terminalreporter: TerminalReporter) -> None:
    if terminalreporter.config.option.pastebin != "failed":
        return
    if "failed" in terminalreporter.stats:
        terminalreporter.write_sep("=", "Sending information to Paste Service")
        for rep in terminalreporter.stats["failed"]:
            try:
                msg = rep.longrepr.reprtraceback.reprentries[-1].reprfileloc
            except AttributeError:
                msg = terminalreporter._getfailureheadline(rep)
            file = StringIO()
            tw = create_terminal_writer(terminalreporter.config, file)
            rep.toterminal(tw)
            s = file.getvalue()
            assert len(s)
            pastebinurl = create_new_paste(s)
            terminalreporter.write_line(f"{msg} --> {pastebinurl}")


def pytest_terminal_summary(terminalreporter: TerminalReporter) -> None:
    durations = terminalreporter.config.option.durations
    durations_min = terminalreporter.config.option.durations_min
    verbose = terminalreporter.config.get_verbosity()
    if durations is None:
        return
    if durations_min is None:
        durations_min = 0.005 if verbose < 2 else 0.0
    tr = terminalreporter
    dlist = []
    for replist in tr.stats.values():
        for rep in replist:
            if hasattr(rep, "duration"):
                dlist.append(rep)
    if not dlist:
        return
    dlist.sort(key=lambda x: x.duration, reverse=True)
    if not durations:
        tr.write_sep("=", "slowest durations")
    else:
        tr.write_sep("=", f"slowest {durations} durations")
        dlist = dlist[:durations]

    for i, rep in enumerate(dlist):
        if rep.duration < durations_min:
            tr.write_line("")
            message = f"({len(dlist) - i} durations < {durations_min:g}s hidden."
            if terminalreporter.config.option.durations_min is None:
                message += "  Use -vv to show these durations."
            message += ")"
            tr.write_line(message)
            break
        tr.write_line(f"{rep.duration:02.2f}s {rep.when:<8} {rep.nodeid}")


def pytest_terminal_summary(
    terminalreporter: TerminalReporter,
) -> Generator[None]:
    config = terminalreporter.config
    with catch_warnings_for_item(
        config=config, ihook=config.hook, when="config", item=None
    ):
        return (yield)

