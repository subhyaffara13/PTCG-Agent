
def test_str_cat_datetime_index_unsorted(join_type):
    # https://github.com/pandas-dev/pandas/pull/62843
    values = [datetime(2024, 1, 1), datetime(2024, 1, 2)]
    s = Series(["a", "b"], index=[values[1], values[0]])
    others = Series(["c", "d"], index=[values[0], values[1]])
    result = s.str.cat(others, join=join_type)
    if join_type in {"outer", "right"}:
        expected = Series(["bc", "ad"], index=[values[0], values[1]])
    else:
        expected = Series(["ad", "bc"], index=[values[1], values[0]])
    tm.assert_series_equal(result, expected)

