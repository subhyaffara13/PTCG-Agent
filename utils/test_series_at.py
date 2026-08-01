
def test_series_at():
    arr = Categorical(["a", "b", "c"])
    ser = Series(arr)
    result = ser.at[0]
    assert result == "a"

