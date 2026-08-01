
def test_32878_int_itemsize():
    # Fixed by GH#45121
    arr = np.arange(5).astype("i4")
    ser = Series(arr)
    val = np.int64(np.iinfo(np.int64).max)
    with pytest.raises(TypeError, match="Invalid value"):
        ser[0] = val

