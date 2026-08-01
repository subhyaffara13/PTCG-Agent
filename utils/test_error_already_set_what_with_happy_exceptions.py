
def test_error_already_set_what_with_happy_exceptions(
    exc_type, exc_value, expected_what
):
    what, py_err_set_after_what = m.error_already_set_what(exc_type, exc_value)
    assert not py_err_set_after_what
    assert what == expected_what

