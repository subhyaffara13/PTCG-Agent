
def test_with_na_groups(any_real_numpy_dtype):
    index = Index(np.arange(10))
    values = Series(np.ones(10), index, dtype=any_real_numpy_dtype)
    labels = Series(
        [np.nan, "foo", "bar", "bar", np.nan, np.nan, "bar", "bar", np.nan, "foo"],
        index=index,
    )

    # this SHOULD be an int
    grouped = values.groupby(labels)
    agged = grouped.agg(len)
    expected = Series([4, 2], index=["bar", "foo"])

    tm.assert_series_equal(agged, expected, check_dtype=False)

    # assert issubclass(agged.dtype.type, np.integer)

    # explicitly return a float from my function
    def f(x):
        return float(len(x))

    agged = grouped.agg(f)
    expected = Series([4.0, 2.0], index=["bar", "foo"])
    if values.dtype == np.float32:
        expected = expected.astype(np.float32)

    tm.assert_series_equal(agged, expected)

