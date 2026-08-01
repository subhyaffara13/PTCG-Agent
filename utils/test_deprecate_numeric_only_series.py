
def test_deprecate_numeric_only_series(dtype, groupby_func, request):
    # GH#46560
    grouper = [0, 0, 1]

    ser = Series([1, 0, 0], dtype=dtype)
    gb = ser.groupby(grouper)

    if groupby_func == "corrwith":
        # corrwith is not implemented on SeriesGroupBy
        assert not hasattr(gb, groupby_func)
        return

    method = getattr(gb, groupby_func)

    expected_ser = Series([1, 0, 0])
    expected_gb = expected_ser.groupby(grouper)
    expected_method = getattr(expected_gb, groupby_func)

    args = get_groupby_method_args(groupby_func, ser)

    fails_on_numeric_object = (
        "corr",
        "cov",
        "cummax",
        "cummin",
        "cumprod",
        "cumsum",
        "quantile",
    )
    # ops that give an object result on object input
    obj_result = (
        "first",
        "last",
        "nth",
        "bfill",
        "ffill",
        "shift",
        "sum",
        "diff",
        "pct_change",
        "var",
        "mean",
        "median",
        "min",
        "max",
        "prod",
        "skew",
        "kurt",
    )

    # Test default behavior; kernels that fail may be enabled in the future but kernels
    # that succeed should not be allowed to fail (without deprecation, at least)
    if groupby_func in fails_on_numeric_object and dtype is object:
        if groupby_func == "quantile":
            msg = "dtype 'object' does not support operation 'quantile'"
        else:
            msg = "is not supported for object dtype"
        with pytest.raises(TypeError, match=msg):
            method(*args)
    elif dtype is object:
        result = method(*args)
        expected = expected_method(*args)
        if groupby_func in obj_result:
            expected = expected.astype(object)
        tm.assert_series_equal(result, expected)

    has_numeric_only = (
        "first",
        "last",
        "max",
        "mean",
        "median",
        "min",
        "prod",
        "quantile",
        "sem",
        "skew",
        "kurt",
        "std",
        "sum",
        "var",
        "cummax",
        "cummin",
        "cumprod",
        "cumsum",
    )
    if groupby_func not in has_numeric_only:
        msg = "got an unexpected keyword argument 'numeric_only'"
        with pytest.raises(TypeError, match=msg):
            method(*args, numeric_only=True)
    elif dtype is object:
        msg = "|".join(
            [
                "SeriesGroupBy.sem called with numeric_only=True and dtype object",
                "Series.skew does not allow numeric_only=True with non-numeric",
                "cum(sum|prod|min|max) is not supported for object dtype",
                r"Cannot use numeric_only=True with SeriesGroupBy\..* and non-numeric",
            ]
        )
        with pytest.raises(TypeError, match=msg):
            method(*args, numeric_only=True)
    elif dtype == bool and groupby_func == "quantile":
        msg = "Cannot use quantile with bool dtype"
        with pytest.raises(TypeError, match=msg):
            # GH#51424
            method(*args, numeric_only=False)
    else:
        result = method(*args, numeric_only=True)
        expected = method(*args, numeric_only=False)
        tm.assert_series_equal(result, expected)

