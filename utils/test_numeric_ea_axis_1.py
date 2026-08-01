
def test_numeric_ea_axis_1(
    method, skipna, min_count, any_numeric_ea_dtype, using_nan_is_na
):
    # GH 54341
    df = DataFrame(
        {
            "a": Series([0, 1, 2, 3], dtype=any_numeric_ea_dtype),
            "b": Series([0, 1, pd.NA, 3], dtype=any_numeric_ea_dtype),
        },
    )
    expected_df = DataFrame(
        {
            "a": [0.0, 1.0, 2.0, 3.0],
            "b": [0.0, 1.0, np.nan, 3.0],
        },
    )
    if method in ("count", "nunique"):
        expected_dtype = "int64"
    elif method in ("all", "any"):
        expected_dtype = "boolean"
    elif method in (
        "kurt",
        "kurtosis",
        "mean",
        "median",
        "sem",
        "skew",
        "std",
        "var",
    ) and not any_numeric_ea_dtype.startswith("Float"):
        expected_dtype = "Float64"
    else:
        expected_dtype = any_numeric_ea_dtype

    kwargs = {}
    if method not in ("count", "nunique", "quantile"):
        kwargs["skipna"] = skipna
    if method in ("prod", "product", "sum"):
        kwargs["min_count"] = min_count

    if not skipna and method in ("idxmax", "idxmin"):
        with pytest.raises(ValueError, match="encountered an NA value"):
            getattr(df, method)(axis=1, **kwargs)
        with pytest.raises(ValueError, match="Encountered an NA value"):
            getattr(expected_df, method)(axis=1, **kwargs)
        return
    result = getattr(df, method)(axis=1, **kwargs)
    expected = getattr(expected_df, method)(axis=1, **kwargs)
    if method not in ("idxmax", "idxmin"):
        if using_nan_is_na:
            expected = expected.astype(expected_dtype)
        else:
            mask = np.isnan(expected)
            expected[mask] = 0
            expected = expected.astype(expected_dtype)
            expected[mask] = pd.NA
    tm.assert_series_equal(result, expected)

