
def test_map_categorical_na_ignore(na_action, expected):
    # GH#47527
    values = pd.Categorical([1, np.nan, 2], categories=[10, 1, 2])
    ser = Series(values)
    result = ser.map({1: 10, np.nan: 42}, na_action=na_action)
    tm.assert_series_equal(result, expected)

