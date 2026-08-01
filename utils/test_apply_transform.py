
def test_apply_transform(ts):
    grouped = ts.groupby(lambda x: x.month, group_keys=False)
    result = grouped.apply(lambda x: x * 2)
    expected = grouped.transform(lambda x: x * 2)
    tm.assert_series_equal(result, expected)

