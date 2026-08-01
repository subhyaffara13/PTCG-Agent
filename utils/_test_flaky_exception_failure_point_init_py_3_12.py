
def _test_flaky_exception_failure_point_init_py_3_12():
    # Behavior change in Python 3.12: https://github.com/python/cpython/issues/102594
    what, py_err_set_after_what = m.error_already_set_what(
        FlakyException, ("failure_point_init",)
    )
    assert not py_err_set_after_what
    lines = what.splitlines()
    assert lines[0].endswith("ValueError[WITH __notes__]: triggered_failure_point_init")
    assert lines[1] == "__notes__ (len=1):"
    assert "Normalization failed:" in lines[2]
    assert "FlakyException" in lines[2]

