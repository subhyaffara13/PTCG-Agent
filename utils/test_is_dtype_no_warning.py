
def test_is_dtype_no_warning(check):
    data = pd.DataFrame({"A": [1, 2]})

    warn = None
    msg = f"{check.__name__} is deprecated"
    if (
        check is is_categorical_dtype
        or check is is_interval_dtype
        or check is is_datetime64tz_dtype
        or check is is_period_dtype
    ):
        warn = DeprecationWarning

    with tm.assert_produces_warning(warn, match=msg):
        check(data)

    with tm.assert_produces_warning(warn, match=msg):
        check(data["A"])

