
def test_is_integer_dtype(dtype):
    assert com.is_integer_dtype(dtype)


def test_is_integer_dtype(data):
    # GH 50667
    pa_type = data.dtype.pyarrow_dtype
    if pa.types.is_integer(pa_type):
        assert is_integer_dtype(data)
    else:
        assert not is_integer_dtype(data)

