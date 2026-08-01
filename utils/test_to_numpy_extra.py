
def test_to_numpy_extra(arr):
    arr[0] = NaT
    original = arr.copy()

    result = arr.to_numpy()
    assert np.isnan(result[0])

    result = arr.to_numpy(dtype="int64")
    assert result[0] == -9223372036854775808

    result = arr.to_numpy(dtype="int64", na_value=0)
    assert result[0] == 0

    result = arr.to_numpy(na_value=arr[1].to_numpy())
    assert result[0] == result[1]

    result = arr.to_numpy(na_value=arr[1].to_numpy(copy=False))
    assert result[0] == result[1]

    tm.assert_equal(arr, original)

