
def test_interval_array_equal(kwargs):
    arr = interval_range(**kwargs).values
    tm.assert_interval_array_equal(arr, arr)

