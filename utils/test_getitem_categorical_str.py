
def test_getitem_categorical_str():
    # GH#31765
    ser = Series(range(5), index=Categorical(["a", "b", "c", "a", "b"]))
    result = ser["a"]
    expected = ser.iloc[[0, 3]]
    tm.assert_series_equal(result, expected)

