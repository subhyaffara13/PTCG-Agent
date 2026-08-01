
def pytest_report_teststatus(  # type:ignore[empty-body]
    report: CollectReport | TestReport, config: Config
) -> TestShortLogReport | tuple[str, str, str | tuple[str, Mapping[str, bool]]]:
    """Return result-category, shortletter and verbose word for status
    reporting.

    The result-category is a category in which to count the result, for
    example "passed", "skipped", "error" or the empty string.

    The shortletter is shown as testing progresses, for example ".", "s",
    "E" or the empty string.

    The verbose word is shown as testing progresses in verbose mode, for
    example "PASSED", "SKIPPED", "ERROR" or the empty string.

    pytest may style these implicitly according to the report outcome.
    To provide explicit styling, return a tuple for the verbose word,
    for example ``"rerun", "R", ("RERUN", {"yellow": True})``.

    :param report: The report object whose status is to be returned.
    :param config: The pytest config object.
    :returns: The test status.

    Stops at first non-None result, see :ref:`firstresult`.

    Use in conftest plugins
    =======================

    Any conftest plugin can implement this hook.
    """


def pytest_report_teststatus(report: BaseReport) -> tuple[str, str, str] | None:
    if report.when in ("setup", "teardown"):
        if report.failed:
            #      category, shortletter, verbose-word
            return "error", "E", "ERROR"
        elif report.skipped:
            return "skipped", "s", "SKIPPED"
        else:
            return "", "", ""
    return None


def pytest_report_teststatus(report: BaseReport) -> tuple[str, str, str] | None:
    if hasattr(report, "wasxfail"):
        if report.skipped:
            return "xfailed", "x", "XFAIL"
        elif report.passed:
            return "xpassed", "X", "XPASS"
    return None


def pytest_report_teststatus(
    report: TestReport,
    config: Config,
) -> tuple[str, str, str | Mapping[str, bool]] | None:
    if report.when != "call":
        return None

    quiet = config.get_verbosity(Config.VERBOSITY_SUBTESTS) == 0
    if isinstance(report, SubtestReport):
        outcome = report.outcome
        description = report._sub_test_description()

        if hasattr(report, "wasxfail"):
            if quiet:
                return "", "", ""
            elif outcome == "skipped":
                category = "xfailed"
                short = "y"  # x letter is used for regular xfail, y for subtest xfail
                status = "SUBXFAIL"
            # outcome == "passed" in an xfail is only possible via a @pytest.mark.xfail mark, which
            # is not applicable to a subtest, which only handles pytest.xfail().
            else:  # pragma: no cover
                # This should not normally happen, unless some plugin is setting wasxfail without
                # the correct outcome. Pytest expects the call outcome to be either skipped or
                # passed in case of xfail.
                # Let's pass this report to the next hook.
                return None
            return category, short, f"{status}{description}"

        if report.failed:
            return outcome, "u", f"SUBFAILED{description}"
        else:
            if report.passed:
                if quiet:
                    return "", "", ""
                else:
                    return f"subtests {outcome}", "u", f"SUBPASSED{description}"
            elif report.skipped:
                if quiet:
                    return "", "", ""
                else:
                    return outcome, "-", f"SUBSKIPPED{description}"

    else:
        failed_subtests_count = config.stash[failed_subtests_key][report.nodeid]
        # Top-level test, fail if it contains failed subtests and it has passed.
        if report.passed and failed_subtests_count > 0:
            report.outcome = "failed"
            suffix = "s" if failed_subtests_count > 1 else ""
            report.longrepr = f"contains {failed_subtests_count} failed subtest{suffix}"

    return None


def pytest_report_teststatus(report: BaseReport) -> tuple[str, str, str]:
    letter = "F"
    if report.passed:
        letter = "."
    elif report.skipped:
        letter = "s"

    outcome: str = report.outcome
    if report.when in ("collect", "setup", "teardown") and outcome == "failed":
        outcome = "error"
        letter = "E"

    return outcome, letter, outcome.upper()

