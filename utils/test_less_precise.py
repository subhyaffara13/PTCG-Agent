
def test_less_precise(data1, data2, any_float_dtype, decimals):
    rtol = 10**-decimals
    s1 = Series([data1], dtype=any_float_dtype)
    s2 = Series([data2], dtype=any_float_dtype)

    if decimals in (5, 10) or (decimals >= 3 and abs(data1 - data2) >= 0.0005):
        msg = "Series values are different"
        with pytest.raises(AssertionError, match=msg):
            tm.assert_series_equal(s1, s2, rtol=rtol)
    else:
        _assert_series_equal_both(s1, s2, rtol=rtol)

