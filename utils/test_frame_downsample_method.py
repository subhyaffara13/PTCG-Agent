import re

def test_frame_downsample_method(
    method, numeric_only, expected_data, using_infer_string
):
    # GH#46442 test if `numeric_only` behave as expected for DataFrameGroupBy

    index = date_range("2018-01-01", periods=2, freq="D")
    expected_index = date_range("2018-12-31", periods=1, freq="YE")
    df = DataFrame({"cat": ["cat_1", "cat_2"], "num": [5, 20]}, index=index)
    resampled = df.resample("YE")
    if numeric_only is lib.no_default:
        kwargs = {}
    else:
        kwargs = {"numeric_only": numeric_only}

    func = getattr(resampled, method)
    if isinstance(expected_data, str):
        if method in ("var", "mean", "median", "prod"):
            klass = TypeError
            msg = re.escape(f"agg function failed [how->{method},dtype->")
            if using_infer_string:
                msg = f"dtype 'str' does not support operation '{method}'"
        elif method in ["sum", "std", "sem"] and using_infer_string:
            klass = TypeError
            msg = f"dtype 'str' does not support operation '{method}'"
        else:
            klass = ValueError
            msg = expected_data
        with pytest.raises(klass, match=msg):
            _ = func(**kwargs)
    else:
        result = func(**kwargs)
        expected = DataFrame(expected_data, index=expected_index)
        tm.assert_frame_equal(result, expected)

