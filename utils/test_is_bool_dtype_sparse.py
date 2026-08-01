
def test_is_bool_dtype_sparse():
    result = is_bool_dtype(Series(SparseArray([True, False])))
    assert result is True

