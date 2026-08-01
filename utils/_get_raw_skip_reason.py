
def _get_raw_skip_reason(report: TestReport) -> str:
    """Get the reason string of a skip/xfail/xpass test report.

    The string is just the part given by the user.
    """
    if hasattr(report, "wasxfail"):
        reason = report.wasxfail
        if reason.startswith("reason: "):
            reason = reason[len("reason: ") :]
        return reason
    else:
        assert report.skipped
        assert isinstance(report.longrepr, tuple)
        _, _, reason = report.longrepr
        if reason.startswith("Skipped: "):
            reason = reason[len("Skipped: ") :]
        elif reason == "Skipped":
            reason = ""
        return reason

