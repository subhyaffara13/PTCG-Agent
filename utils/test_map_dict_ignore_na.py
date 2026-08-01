
def test_map_dict_ignore_na(arg_func):
    # GH#47527
    mapping = arg_func({1: 10, np.nan: 42})
    ser = Series([1, np.nan, 2])
    result = ser.map(mapping, na_action="ignore")
    expected = Series([10, np.nan, np.nan])
    tm.assert_series_equal(result, expected)

