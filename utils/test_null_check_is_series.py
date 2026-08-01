
def test_null_check_is_series(null_func, ser):
    assert isinstance(null_func(ser), Series)

