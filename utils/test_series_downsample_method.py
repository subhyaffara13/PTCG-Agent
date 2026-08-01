
def test_series_downsample_method(
    method, numeric_only, expected_data, using_infer_string
):
    # GH#46442 test if `numeric_only` behave as expected for SeriesGroupBy

    index = date_range("2018-01-01", periods=2, freq="D")
    expected_index = date_range("2018-12-31", periods=1, freq="YE")
    df = Series(["cat_1", "cat_2"], index=index)
    resampled = df.resample("YE")
    kwargs = {} if numeric_only is lib.no_default else {"numeric_only": numeric_only}

    func = getattr(resampled, method)
    if numeric_only and numeric_only is not lib.no_default:
        msg = rf"Cannot use numeric_only=True with SeriesGroupBy\.{method}"
        with pytest.raises(TypeError, match=msg):
            func(**kwargs)
    elif method == "prod":
        msg = re.escape("agg function failed [how->prod,dtype->")
        if using_infer_string:
            msg = "dtype 'str' does not support operation 'prod'"
        with pytest.raises(TypeError, match=msg):
            func(**kwargs)

    else:
        result = func(**kwargs)
        expected = Series(expected_data, index=expected_index)
        tm.assert_series_equal(result, expected)

