
def test_directional_stats(dtype, xp, devices):
    dtype = getattr(xp, dtype)
    for device in devices:
        x = get_arrays(1, shape=(30, 3), device=device, dtype=dtype, xp=xp)[0]
        res = stats.directional_stats(x)
        assert xp_device(res.mean_direction) == xp_device(x)
        assert res.mean_direction.dtype == dtype
        assert xp_device(res.mean_resultant_length) == xp_device(x)
        assert res.mean_resultant_length.dtype == dtype


def test_directional_stats(normalize, axis, xp):
    mxp, marrays, narrays = get_arrays(1, shape=(19, 20, 3), xp=xp)
    res = stats.directional_stats(*marrays, normalize=normalize, axis=axis)

    x, = narrays
    if axis == 0:
        x = np.swapaxes(x, 0, 1)

    for i in range(x.shape[0]):
        xi = x[i]
        xi = xi[~np.any(np.isnan(xi), axis=-1), :]
        ref = stats.directional_stats(xi, normalize=normalize)
        xp_assert_close(res.mean_direction.data[i, ...],
                        xp.asarray(ref.mean_direction))
        xp_assert_close(res.mean_resultant_length.data[i],
                        xp.asarray(ref.mean_resultant_length)[()])
    assert not xp.any(res.mean_direction.mask)
    assert not xp.any(res.mean_resultant_length.mask)

