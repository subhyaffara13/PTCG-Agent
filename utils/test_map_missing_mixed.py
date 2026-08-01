
def test_map_missing_mixed(vals, mapping, exp):
    # GH20495
    s = Series([*vals, np.nan])
    result = s.map(mapping)
    exp = Series(exp)
    tm.assert_series_equal(result, exp)

