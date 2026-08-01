
def test_from_sparse_dtype():
    dtype = SparseDtype("float", 0)
    result = SparseDtype(dtype)
    assert result.fill_value == 0

