
def test_get_dtype_error_catch(func):
    # see gh-15941
    #
    # No exception should be raised.

    msg = f"{func.__name__} is deprecated"
    warn = None
    if (
        func is com.is_int64_dtype
        or func is com.is_interval_dtype
        or func is com.is_datetime64tz_dtype
        or func is com.is_categorical_dtype
        or func is com.is_period_dtype
    ):
        warn = Pandas4Warning

    with tm.assert_produces_warning(warn, match=msg):
        assert not func(None)

