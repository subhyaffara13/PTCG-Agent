
def test_apply_with_string_funcs(float_frame, func, kwds, how):
    result = getattr(float_frame, how)(func, **kwds)
    expected = getattr(float_frame, func)(**kwds)
    tm.assert_series_equal(result, expected)

