
def _test_flaky_exception_failure_point_init_before_py_3_12():
    with pytest.raises(RuntimeError) as excinfo:
        m.error_already_set_what(FlakyException, ("failure_point_init",))
    lines = str(excinfo.value).splitlines()
    # PyErr_NormalizeException replaces the original FlakyException with ValueError:
    assert lines[:3] == [
        "pybind11::error_already_set: MISMATCH of original and normalized active exception types:"
        " ORIGINAL FlakyException REPLACED BY ValueError: triggered_failure_point_init",
        "",
        "At:",
    ]
    # Checking the first two lines of the traceback as formatted in error_string():
    assert "test_exceptions.py(" in lines[3]
    assert lines[3].endswith("): __init__")
    assert lines[4].endswith(
        "): _test_flaky_exception_failure_point_init_before_py_3_12"
    )

