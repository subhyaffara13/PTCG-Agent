
def test_xmean(fun, kwargs, dtype, xp, devices):
    dtype = getattr(xp, dtype)
    for device in devices:
        x, weights = get_arrays(2, device=device, dtype=dtype, xp=xp)
        res = fun(x, weights=weights, **kwargs)
        assert xp_device(res) == xp_device(x)
        assert x.dtype == dtype

