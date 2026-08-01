
def test_is_bool_dtype_numpy_error():
    # GH39010
    assert not com.is_bool_dtype("0 - Name")

