
def test_to_numpy_kwargs_raises():
    # numpy
    s = Series([1, 2, 3])
    msg = r"to_numpy\(\) got an unexpected keyword argument 'foo'"
    with pytest.raises(TypeError, match=msg):
        s.to_numpy(foo=True)

    # extension
    s = Series([1, 2, 3], dtype="Int64")
    with pytest.raises(TypeError, match=msg):
        s.to_numpy(foo=True)

