
def test_infer_dtype_from_python_scalar(data, exp_dtype):
    dtype, val = infer_dtype_from_scalar(data)
    assert dtype == exp_dtype

