
def test_nunique_with_empty_series():
    # GH 12553
    data = Series(name="name", dtype=object)
    result = data.groupby(level=0).nunique()
    expected = Series(name="name", dtype="int64")
    tm.assert_series_equal(result, expected)

