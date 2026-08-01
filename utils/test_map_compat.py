
def test_map_compat():
    # related GH 8024
    s = Series([True, True, False], index=[1, 2, 3])
    result = s.map({True: "foo", False: "bar"})
    expected = Series(["foo", "foo", "bar"], index=[1, 2, 3])
    tm.assert_series_equal(result, expected)

