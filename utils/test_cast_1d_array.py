
def test_cast_1d_array(datum1, datum2):
    data = [datum1, datum2]
    result = construct_1d_object_array_from_listlike(data)

    # Direct comparison fails: https://github.com/numpy/numpy/issues/10218
    assert result.dtype == "object"
    assert list(result) == data

