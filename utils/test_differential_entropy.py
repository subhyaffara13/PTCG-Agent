
def test_differential_entropy(method, dtype, xp, devices):
    dtype = getattr(xp, dtype)
    for device in devices:
        values = get_arrays(1, device=device, dtype=dtype, xp=xp)[0]
        res = stats.differential_entropy(values, method=method)
        assert xp_device(res) == xp_device(values)
        assert values.dtype == dtype

