
def test_dtype_to_arrow_c_fmt(pandas_dtype, c_string):  # PR01
    """Test ``dtype_to_arrow_c_fmt`` utility function."""
    assert dtype_to_arrow_c_fmt(pandas_dtype) == c_string

