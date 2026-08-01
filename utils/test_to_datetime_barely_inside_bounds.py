
def test_to_datetime_barely_inside_bounds(timestamp):
    # see gh-57150
    result, _ = tslib.array_to_datetime(np.array([timestamp], dtype=object))
    tm.assert_numpy_array_equal(result, np.array([timestamp], dtype="M8[ns]"))

