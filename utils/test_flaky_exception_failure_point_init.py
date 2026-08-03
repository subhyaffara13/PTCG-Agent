import sys

def test_flaky_exception_failure_point_init():
    if sys.version_info[:2] < (3, 12):
        _test_flaky_exception_failure_point_init_before_py_3_12()
    else:
        _test_flaky_exception_failure_point_init_py_3_12()

