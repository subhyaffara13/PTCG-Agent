
def test_multiply_two_string_raises():
    arr = np.array(["hello", "world"], dtype="T")
    with pytest.raises(np._core._exceptions._UFuncNoLoopError):
        np.multiply(arr, arr)

