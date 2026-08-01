
def test_infer_dtype_from_float_scalar(float_numpy_dtype):
    float_numpy_dtype = np.dtype(float_numpy_dtype).type
    data = float_numpy_dtype(12)

    dtype, val = infer_dtype_from_scalar(data)
    assert dtype == float_numpy_dtype

