
def test_is_unsigned_integer_dtype(dtype):
    assert com.is_unsigned_integer_dtype(dtype)


def test_is_unsigned_integer_dtype(data):
    pa_type = data.dtype.pyarrow_dtype
    if pa.types.is_unsigned_integer(pa_type):
        assert is_unsigned_integer_dtype(data)
    else:
        assert not is_unsigned_integer_dtype(data)

