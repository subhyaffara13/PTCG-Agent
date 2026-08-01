
def test_groupby_unit64_float_conversion():
    # GH: 30859 groupby converts unit64 to floats sometimes
    df = DataFrame({"first": [1], "second": [1], "value": [16148277970000000000]})
    result = df.groupby(["first", "second"])["value"].max()
    expected = Series(
        [16148277970000000000],
        MultiIndex.from_product([[1], [1]], names=["first", "second"]),
        name="value",
    )
    tm.assert_series_equal(result, expected)

