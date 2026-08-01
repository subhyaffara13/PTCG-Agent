
def test_groupby_last_first_preserve_categoricaldtype(func):
    # GH#33090
    df = DataFrame({"a": [1, 2, 3]})
    df["b"] = df["a"].astype("category")
    result = getattr(df.groupby("a")["b"], func)()
    expected = Series(
        Categorical([1, 2, 3]), name="b", index=Index([1, 2, 3], name="a")
    )
    tm.assert_series_equal(expected, result)

