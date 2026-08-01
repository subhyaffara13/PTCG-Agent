
def test_flaky_exception_failure_point_str():
    what, py_err_set_after_what = m.error_already_set_what(
        FlakyException, ("failure_point_str",)
    )
    assert not py_err_set_after_what
    lines = what.splitlines()
    n = 3 if env.PYPY and len(lines) == 3 else 5
    assert (
        lines[:n]
        == [
            "FlakyException: <MESSAGE UNAVAILABLE DUE TO ANOTHER EXCEPTION>",
            "",
            "MESSAGE UNAVAILABLE DUE TO EXCEPTION: ValueError: triggered_failure_point_str",
            "",
            "At:",
        ][:n]
    )

