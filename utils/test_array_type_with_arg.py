
def test_array_type_with_arg(dtype):
    assert dtype.construct_array_type() is SparseArray

