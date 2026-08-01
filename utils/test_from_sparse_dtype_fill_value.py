
def test_from_sparse_dtype_fill_value():
    dtype = SparseDtype("int", 1)
    result = SparseDtype(dtype, fill_value=2)
    expected = SparseDtype("int", 2)
    assert result == expected

