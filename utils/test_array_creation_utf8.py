
def test_array_creation_utf8(dtype, data):
    arr = np.array(data, dtype=dtype)
    assert str(arr) == "[" + " ".join(["'" + str(d) + "'" for d in data]) + "]"
    assert arr.dtype == dtype

