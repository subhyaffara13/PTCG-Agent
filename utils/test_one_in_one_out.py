
def test_one_in_one_out(fun, kwargs, dtype, xp, devices):
    dtype = getattr(xp, dtype)
    for device in devices:
        array = get_arrays(1, device=device, dtype=dtype, xp=xp)[0]
        res = fun(array, **kwargs)
        assert xp_device(res) == xp_device(array)
        assert res.dtype == dtype

