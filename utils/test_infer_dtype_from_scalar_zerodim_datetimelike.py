
def test_infer_dtype_from_scalar_zerodim_datetimelike(cls):
    # ndarray.item() can incorrectly return int instead of td64/dt64
    val = cls(1234, "ns")
    arr = np.array(val)

    dtype, res = infer_dtype_from_scalar(arr)
    assert dtype.type is cls
    assert isinstance(res, cls)

    dtype, res = infer_dtype_from(arr)
    assert dtype.type is cls

