
def test_one_sample_reducing(fun, kwargs, axis, xp):
    mxp, marrays, narrays = get_arrays(1, xp=xp)
    kwargs = dict(axis=axis) | kwargs
    res = fun(marrays[0], **kwargs)
    ref = fun(narrays[0], nan_policy='omit', **kwargs)
    xp_assert_close(res.data, xp.asarray(ref))

