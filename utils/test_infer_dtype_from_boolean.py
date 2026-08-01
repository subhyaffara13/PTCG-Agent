
def test_infer_dtype_from_boolean(bool_val):
    dtype, val = infer_dtype_from_scalar(bool_val)
    assert dtype == np.bool_

