
def test_map_empty_integer_series():
    # GH52384
    s = Series([], dtype=int)
    result = s.map(lambda x: x)
    tm.assert_series_equal(result, s)

