
def check_filtfilt_gust(b, a, shape, axis, irlen=None):
    # Generate x, the data to be filtered.
    rng = np.random.default_rng(123)
    x = rng.standard_normal(shape)

    # Apply filtfilt to x. This is the main calculation to be checked.
    y = filtfilt(b, a, x, axis=axis, method="gust", irlen=irlen)

    # Also call the private function so we can test the ICs.
    yg, zg1, zg2 = _filtfilt_gust(b, a, x, axis=axis, irlen=irlen)

    # filtfilt_gust_opt is an independent implementation that gives the
    # expected result, but it only handles 1-D arrays, so use some looping
    # and reshaping shenanigans to create the expected output arrays.
    xx = np.swapaxes(x, axis, -1)
    out_shape = xx.shape[:-1]
    yo = np.empty_like(xx)
    m = max(len(a), len(b)) - 1
    zo1 = np.empty(out_shape + (m,))
    zo2 = np.empty(out_shape + (m,))
    for indx in product(*[range(d) for d in out_shape]):
        yo[indx], zo1[indx], zo2[indx] = filtfilt_gust_opt(b, a, xx[indx])
    yo = np.swapaxes(yo, -1, axis)
    zo1 = np.swapaxes(zo1, -1, axis)
    zo2 = np.swapaxes(zo2, -1, axis)

    xp_assert_close(y, yo, rtol=1e-8, atol=1e-9)
    xp_assert_close(yg, yo, rtol=1e-8, atol=1e-9)
    xp_assert_close(zg1, zo1, rtol=1e-8, atol=1e-9)
    xp_assert_close(zg2, zo2, rtol=1e-8, atol=1e-9)

