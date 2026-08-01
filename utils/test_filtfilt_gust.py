
def test_filtfilt_gust():
    # Design a filter.
    z, p, k = signal.ellip(3, 0.01, 120, 0.0875, output='zpk')

    # Find the approximate impulse response length of the filter.
    eps = 1e-10
    r = np.max(np.abs(p))
    approx_impulse_len = int(np.ceil(np.log(eps) / np.log(r)))

    b, a = zpk2tf(z, p, k)
    for irlen in [None, approx_impulse_len]:
        signal_len = 5 * approx_impulse_len

        # 1-d test case
        check_filtfilt_gust(b, a, (signal_len,), 0, irlen)

        # 3-d test case; test each axis.
        for axis in range(3):
            shape = [2, 2, 2]
            shape[axis] = signal_len
            check_filtfilt_gust(b, a, shape, axis, irlen)

    # Test case with length less than 2*approx_impulse_len.
    # In this case, `filtfilt_gust` should behave the same as if
    # `irlen=None` was given.
    length = 2*approx_impulse_len - 50
    check_filtfilt_gust(b, a, (length,), 0, approx_impulse_len)

