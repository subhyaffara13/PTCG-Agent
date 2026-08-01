
def test_pyarrow_string_import_error(name, dtype):
    # GH-44276
    assert not com.is_dtype_equal(dtype, "string[pyarrow]")

