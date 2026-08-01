
def test_frame_consistency(groupby_func):
    # GH#48028
    if groupby_func in ("first", "last"):
        msg = "first and last don't exist for DataFrame anymore"
        pytest.skip(reason=msg)

    if groupby_func in ("cumcount", "ngroup"):
        assert not hasattr(DataFrame, groupby_func)
        return

    frame_method = getattr(DataFrame, groupby_func)
    gb_method = getattr(DataFrameGroupBy, groupby_func)
    result = set(inspect.signature(gb_method).parameters)
    if groupby_func == "size":
        # "size" is a method on GroupBy but property on DataFrame:
        expected = {"self"}
    else:
        expected = set(inspect.signature(frame_method).parameters)

    # Exclude certain arguments from result and expected depending on the operation
    # Some of these may be purposeful inconsistencies between the APIs
    exclude_expected, exclude_result = set(), set()
    if groupby_func in ("any", "all"):
        exclude_expected = {"kwargs", "bool_only", "axis"}
    elif groupby_func in ("count",):
        exclude_expected = {"numeric_only", "axis"}
    elif groupby_func in ("nunique",):
        exclude_expected = {"axis"}
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
        exclude_expected = {"axis", "skipna", "args"}
    elif groupby_func in ("cumprod", "cumsum"):
        exclude_expected = {"axis", "skipna"}
    elif groupby_func in ("pct_change",):
        exclude_expected = {"kwargs"}
    elif groupby_func in ("rank",):
        exclude_expected = {"numeric_only"}
    elif groupby_func in ("quantile",):
        exclude_expected = {"method", "axis"}
    elif groupby_func in ["corrwith"]:
        exclude_expected = {"min_periods"}
    if groupby_func not in ["pct_change", "size"]:
        exclude_expected |= {"axis"}

    # Ensure excluded arguments are actually in the signatures
    assert result & exclude_result == exclude_result
    assert expected & exclude_expected == exclude_expected

    result -= exclude_result
    expected -= exclude_expected
    assert result == expected

