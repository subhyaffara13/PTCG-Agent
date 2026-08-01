
def test_one_sample_weighted_reducing(fun, kwargs, weighted, axis, xp):
    mxp, marrays, narrays = get_arrays(2, xp=xp)
    mweights = marrays[1] if weighted else None
    nweights = narrays[1] if weighted else None
    res = fun(marrays[0], weights=mweights, axis=axis, **kwargs)
    ref = fun(narrays[0], weights=nweights, nan_policy='omit', axis=axis, **kwargs)
    xp_assert_close(res.data, xp.asarray(ref))

