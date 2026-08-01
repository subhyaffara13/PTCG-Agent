
def test_bad_reduce_raises():
    arr = np.array([1, 2, 3], dtype="int64")
    arr = NumpyExtensionArray(arr)
    msg = "cannot perform not_a_method with type int"
    with pytest.raises(TypeError, match=msg):
        arr._reduce(msg)

