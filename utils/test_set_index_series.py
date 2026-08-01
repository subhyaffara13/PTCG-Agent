
def test_set_index_series():
    df = DataFrame({"a": [1, 2], "b": 1.5})
    ser = Series([10, 11])
    df = df.set_index(ser)
    expected = df.index.copy(deep=True)
    ser.iloc[0] = 100
    tm.assert_index_equal(df.index, expected)

