
def test_groupby_series_with_tuple_name():
    # GH 37755
    ser = Series([1, 2, 3, 4], index=[1, 1, 2, 2], name=("a", "a"))
    ser.index.name = ("b", "b")
    result = ser.groupby(level=0).last()
    expected = Series([2, 4], index=[1, 2], name=("a", "a"))
    expected.index.name = ("b", "b")
    tm.assert_series_equal(result, expected)

