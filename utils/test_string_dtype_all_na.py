
def test_string_dtype_all_na(
    string_dtype_no_object, reduction_func, skipna, min_count, test_series
):
    # https://github.com/pandas-dev/pandas/issues/60985
    if reduction_func == "corrwith":
        # corrwith is deprecated.
        return

    dtype = string_dtype_no_object

    if reduction_func in [
        "any",
        "all",
        "idxmin",
        "idxmax",
        "mean",
        "median",
        "std",
        "var",
    ]:
        kwargs = {"skipna": skipna}
    elif reduction_func in ["kurt"]:
        kwargs = {"min_count": min_count}
    elif reduction_func in ["count", "nunique", "quantile", "sem", "size"]:
        kwargs = {}
    else:
        kwargs = {"skipna": skipna, "min_count": min_count}

    expected_dtype, expected_value = dtype, pd.NA
    if reduction_func in ["all", "any"]:
        expected_dtype = "bool"
        # TODO: For skipna=False, bool(pd.NA) raises; should groupby?
        expected_value = not skipna if reduction_func == "any" else True
    elif reduction_func in ["count", "nunique", "size"]:
        # TODO: Should be more consistent - return Int64 when dtype.na_value is pd.NA?
        if (
            test_series
            and reduction_func == "size"
            and dtype.storage == "pyarrow"
            and dtype.na_value is pd.NA
        ):
            expected_dtype = "Int64"
        else:
            expected_dtype = "int64"
        expected_value = 1 if reduction_func == "size" else 0
    elif not skipna or min_count > 0:
        expected_value = pd.NA
    elif reduction_func == "sum":
        # https://github.com/pandas-dev/pandas/pull/60936
        expected_value = ""

    df = DataFrame({"a": ["x"], "b": [pd.NA]}, dtype=dtype)
    obj = df["b"] if test_series else df
    args = get_groupby_method_args(reduction_func, obj)
    gb = obj.groupby(df["a"])
    method = getattr(gb, reduction_func)

    if reduction_func in [
        "mean",
        "median",
        "kurt",
        "prod",
        "quantile",
        "sem",
        "skew",
        "std",
        "var",
    ]:
        msg = f"dtype '{dtype}' does not support operation '{reduction_func}'"
        with pytest.raises(TypeError, match=msg):
            method(*args, **kwargs)
        return
    elif reduction_func in ["idxmin", "idxmax"]:
        if skipna:
            msg = f"{reduction_func} with skipna=True encountered all NA values"
        else:
            msg = f"{reduction_func} with skipna=False encountered an NA value."
        with pytest.raises(ValueError, match=msg):
            method(*args, **kwargs)
        return

    result = method(*args, **kwargs)
    index = pd.Index(["x"], name="a", dtype=dtype)
    if test_series or reduction_func == "size":
        name = None if not test_series and reduction_func == "size" else "b"
        expected = Series(expected_value, index=index, dtype=expected_dtype, name=name)
    else:
        expected = DataFrame({"b": expected_value}, index=index, dtype=expected_dtype)
    tm.assert_equal(result, expected)

