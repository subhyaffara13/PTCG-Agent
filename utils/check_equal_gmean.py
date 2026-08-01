
def check_equal_gmean(array_like, desired, axis=None, dtype=None, rtol=1e-7):
    # Note this doesn't test when axis is not specified
    x = mstats.gmean(array_like, axis=axis, dtype=dtype)
    assert_allclose(x, desired, rtol=rtol)
    assert_equal(x.dtype, dtype)


def check_equal_gmean(*args, **kwargs):
    return check_equal_xmean(*args, mean_fun=stats.gmean, **kwargs)

