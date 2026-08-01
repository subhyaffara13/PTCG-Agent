
def test_zscore(fun, dtype, xp, devices):
    dtype = getattr(xp, dtype)
    for device in devices:
        n = 2 if (fun == stats.zmap) else 1
        arrays = get_arrays(n, device=device, dtype=dtype, xp=xp)
        res = fun(*arrays)
        assert xp_device(res) == xp_device(arrays[0])
        assert res.dtype == dtype

