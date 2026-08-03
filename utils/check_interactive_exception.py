import sys

def check_interactive_exception(call: CallInfo[object], report: BaseReport) -> bool:
    """Check whether the call raised an exception that should be reported as
    interactive."""
    if call.excinfo is None:
        # Didn't raise.
        return False
    if hasattr(report, "wasxfail"):
        # Exception was expected.
        return False
    unittest = sys.modules.get("unittest")
    if isinstance(call.excinfo.value, Skipped | bdb.BdbQuit) or (
        unittest is not None and isinstance(call.excinfo.value, unittest.SkipTest)
    ):
        # Special control flow exception.
        return False
    return True

