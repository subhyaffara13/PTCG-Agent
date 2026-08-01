
def test_apply_funcs_over_empty(func):
    # GH 28213
    df = DataFrame(columns=["a", "b", "c"])

    result = df.apply(getattr(np, func))
    expected = getattr(df, func)()
    if func in ("sum", "prod"):
        expected = expected.astype(float)
    tm.assert_series_equal(result, expected)

