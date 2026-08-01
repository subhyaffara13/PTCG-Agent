
def test_infer_dtype_from_complex(complex_dtype):
    data = np.dtype(complex_dtype).type(1)
    dtype, val = infer_dtype_from_scalar(data)
    assert dtype == np.complex128

