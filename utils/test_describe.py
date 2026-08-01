
def test_describe(dtype, xp, devices):
    dtype = getattr(xp, dtype)
    for device in devices:
        array = get_arrays(1, shape=10, dtype=dtype, device=device, xp=xp)[0]
        res = stats.describe(array, axis=-1)

        assert xp_device(res.nobs) == xp_device(array)
        assert xp_device(res.minmax[0]) == xp_device(array)
        assert xp_device(res.minmax[1]) == xp_device(array)
        assert xp_device(res.variance) == xp_device(array)
        assert xp_device(res.skewness) == xp_device(array)
        assert xp_device(res.kurtosis) == xp_device(array)

        assert res.minmax[0].dtype == dtype
        assert res.minmax[1].dtype == dtype
        assert res.variance.dtype == dtype
        assert res.skewness.dtype == dtype
        assert res.kurtosis.dtype == dtype


def test_describe(axis, kwargs, xp):
    mxp, marrays, narrays = get_arrays(1, xp=xp)
    kwargs = dict(axis=axis) | kwargs
    res = stats.describe(marrays[0], **kwargs)
    ref = stats.describe(narrays[0], nan_policy='omit', **kwargs)
    xp_assert_close(res.nobs.data, xp.asarray(ref.nobs))
    xp_assert_close(res.minmax[0].data, xp.asarray(ref.minmax[0].data))
    xp_assert_close(res.minmax[1].data, xp.asarray(ref.minmax[1].data))
    # copy reference arrays due to torch complaint about non-writeable buffer
    xp_assert_close(res.variance.data,
                    xp.asarray(np.asarray(ref.variance.data, copy=True)))
    xp_assert_close(res.skewness.data,
                    xp.asarray(np.asarray(ref.skewness.data, copy=True)))
    xp_assert_close(res.kurtosis.data,
                    xp.asarray(np.asarray(ref.kurtosis.data, copy=True)))

