
def test_boxcox_llf(dtype, xp, devices):
    dtype = getattr(xp, dtype)
    for device in devices:
        data = get_arrays(1, device=device, dtype=dtype, xp=xp)[0]
        res = stats.boxcox_llf(1, data)
        assert xp_device(res) == xp_device(data)
        assert data.dtype == dtype

