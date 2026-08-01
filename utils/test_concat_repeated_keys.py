
def test_concat_repeated_keys(keys, integrity):
    # GH: 20816
    series_list = [Series({"a": 1}), Series({"b": 2}), Series({"c": 3})]
    result = concat(series_list, keys=keys, verify_integrity=integrity)
    tuples = list(zip(keys, ["a", "b", "c"]))
    expected = Series([1, 2, 3], index=MultiIndex.from_tuples(tuples))
    tm.assert_series_equal(result, expected)

