
def test_setitem_validates(cls, dtype):
    arr = cls._from_sequence(["a", "b"], dtype=dtype)

    msg = "Invalid value '10' for dtype 'str"
    with pytest.raises(TypeError, match=msg):
        arr[0] = 10

    msg = "Invalid value for dtype 'str"
    with pytest.raises(TypeError, match=msg):
        arr[:] = np.array([1, 2])

