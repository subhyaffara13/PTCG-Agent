
def test_infer_dtype_from_timedelta():
    td64 = np.timedelta64(1, "ns")
    dtype, val = infer_dtype_from_scalar(td64)
    assert dtype == "m8[ns]"

    pytd = timedelta(1)
    dtype, val = infer_dtype_from_scalar(pytd)
    assert dtype == "m8[us]"

    td = Timedelta(1)
    dtype, val = infer_dtype_from_scalar(td)
    assert dtype == "m8[ns]"

