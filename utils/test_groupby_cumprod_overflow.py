
def test_groupby_cumprod_overflow():
    # GH#37493 if we overflow we return garbage consistent with numpy
    df = DataFrame({"key": ["b"] * 4, "value": 100_000})
    actual = df.groupby("key")["value"].cumprod()
    expected = Series(
        [100_000, 10_000_000_000, 1_000_000_000_000_000, 7766279631452241920],
        name="value",
    )
    tm.assert_series_equal(actual, expected)

    numpy_result = df.groupby("key", group_keys=False)["value"].apply(
        lambda x: x.cumprod()
    )
    numpy_result.name = "value"
    tm.assert_series_equal(actual, numpy_result)

