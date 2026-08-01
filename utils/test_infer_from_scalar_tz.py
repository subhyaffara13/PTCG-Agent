
def test_infer_from_scalar_tz(tz):
    dt = Timestamp(1, tz=tz)
    dtype, val = infer_dtype_from_scalar(dt)

    exp_dtype = f"datetime64[ns, {tz}]"

    assert dtype == exp_dtype
    assert val == dt

