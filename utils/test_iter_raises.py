
def test_iter_raises():
    # GH 54173
    ser = Series(["foo", "bar"])
    with pytest.raises(TypeError, match="'StringMethods' object is not iterable"):
        iter(ser.str)

