
def check_equal_hmean(array_like, desired, axis=None, dtype=None, rtol=1e-7):
    x = stats.hmean(array_like, axis=axis, dtype=dtype)
    assert_allclose(x, desired, rtol=rtol)
    assert_equal(x.dtype, dtype)


def check_equal_hmean(*args, **kwargs):
    return check_equal_xmean(*args, mean_fun=stats.hmean, **kwargs)

