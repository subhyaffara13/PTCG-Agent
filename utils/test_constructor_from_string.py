
def test_constructor_from_string():
    result = NumpyEADtype.construct_from_string("int64")
    expected = NumpyEADtype(np.dtype("int64"))
    assert result == expected

