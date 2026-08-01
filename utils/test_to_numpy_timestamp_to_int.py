
def test_to_numpy_timestamp_to_int():
    # GH 55997
    ser = pd.Series(["2020-01-01 04:30:00"], dtype="timestamp[ns][pyarrow]")
    result = ser.to_numpy(dtype=np.int64)
    expected = np.array([1577853000000000000])
    tm.assert_numpy_array_equal(result, expected)

