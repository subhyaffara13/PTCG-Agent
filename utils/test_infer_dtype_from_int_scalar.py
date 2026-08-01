
def test_infer_dtype_from_int_scalar(any_int_numpy_dtype):
    # Test that infer_dtype_from_scalar is
    # returning correct dtype for int and float.
    data = np.dtype(any_int_numpy_dtype).type(12)
    dtype, val = infer_dtype_from_scalar(data)
    assert dtype == type(data)

