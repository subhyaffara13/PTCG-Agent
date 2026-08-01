
def test_infer_dtype_misc():
    dt = date(2000, 1, 1)
    dtype, val = infer_dtype_from_scalar(dt)
    assert dtype == np.object_

    ts = Timestamp(1, tz="US/Eastern")
    dtype, val = infer_dtype_from_scalar(ts)
    assert dtype == "datetime64[ns, US/Eastern]"

