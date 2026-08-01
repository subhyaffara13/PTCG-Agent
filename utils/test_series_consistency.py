
def test_series_consistency(request, groupby_func):
    # GH#48028
    if groupby_func in ("first", "last"):
        msg = "first and last don't exist for Series anymore"
        pytest.skip(msg)

    if groupby_func in ("cumcount", "corrwith", "ngroup"):
        assert not hasattr(Series, groupby_func)
        return

    series_method = getattr(Series, groupby_func)
    gb_method = getattr(SeriesGroupBy, groupby_func)
    result = set(inspect.signature(gb_method).parameters)
    if groupby_func == "size":
        # "size" is a method on GroupBy but property on Series
        expected = {"self"}
    else:
        expected = set(inspect.signature(series_method).parameters)

    # Exclude certain arguments from result and expected depending on the operation
    # Some of these may be purposeful inconsistencies between the APIs
    exclude_expected, exclude_result = set(), set()
    if groupby_func in ("any", "all"):
        exclude_expected = {"kwargs", "bool_only", "axis"}
    elif groupby_func in ("max", "min"):
        exclude_expected = {"axis", "kwargs"}
        exclude_result = {"min_count", "engine", "engine_kwargs"}
    elif groupby_func in ("sum", "mean", "std", "var"):
        exclude_expected = {"axis", "kwargs"}
        exclude_result = {"engine", "engine_kwargs"}
    elif groupby_func in ("median", "prod", "sem"):
        exclude_expected = {"axis", "kwargs"}
    elif groupby_func in ("bfill", "ffill"):
        exclude_expected = {"inplace", "axis", "limit_area"}
    elif groupby_func in ("cummax", "cummin"):
        exclude_expected = {"skipna", "args"}
        exclude_result = {"numeric_only"}
    elif groupby_func in ("cumprod", "cumsum"):
        exclude_expected = {"skipna"}
        exclude_result = {"numeric_only"}
    elif groupby_func in ("pct_change",):
        exclude_expected = {"kwargs"}
    elif groupby_func in ("rank",):
        exclude_expected = {"numeric_only"}
    elif groupby_func in ("idxmin", "idxmax"):
        exclude_expected = {"args", "kwargs"}
    elif groupby_func in ("quantile",):
        exclude_result = {"numeric_only"}
    if groupby_func not in [
        "diff",
        "pct_change",
        "count",
        "nunique",
        "quantile",
        "size",
    ]:
        exclude_expected |= {"axis"}

    # Ensure excluded arguments are actually in the signatures
    assert result & exclude_result == exclude_result
    assert expected & exclude_expected == exclude_expected

    result -= exclude_result
    expected -= exclude_expected
    assert result == expected

