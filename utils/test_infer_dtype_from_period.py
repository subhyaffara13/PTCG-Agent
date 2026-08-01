
def test_infer_dtype_from_period(freq):
    p = Period("2011-01-01", freq=freq)
    dtype, val = infer_dtype_from_scalar(p)

    exp_dtype = f"period[{freq}]"

    assert dtype == exp_dtype
    assert val == p

