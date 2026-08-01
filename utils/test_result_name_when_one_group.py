
def test_result_name_when_one_group(name):
    # GH 46369
    ser = Series([1, 2], name=name)
    result = ser.groupby(["a", "a"], group_keys=False).apply(lambda x: x)
    expected = Series([1, 2], name=name)

    tm.assert_series_equal(result, expected)

