
def test_32878_complex_itemsize():
    arr = np.arange(5).astype("c8")
    ser = Series(arr)
    val = np.finfo(np.float64).max
    val = val.astype("c16")

    # GH#32878 used to coerce val to inf+0.000000e+00j
    with pytest.raises(TypeError, match="Invalid value"):
        ser[0] = val

