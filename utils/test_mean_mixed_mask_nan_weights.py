
def test_mean_mixed_mask_nan_weights(weighted_fun_name, unpacker):
    # targeted test of _axis_nan_policy_factory with 2D masked sample:
    # omitting samples with masks and nan_policy='omit' are equivalent
    # also checks paired-sample sentinel value removal

    if weighted_fun_name == 'pmean':
        def weighted_fun(a, **kwargs):
            return stats.pmean(a, p=0.42, **kwargs)
    else:
        weighted_fun = getattr(stats, weighted_fun_name)

    def func(*args, **kwargs):
        return unpacker(weighted_fun(*args, **kwargs))

    m, n = 3, 20
    axis = -1

    rng = np.random.default_rng(6541968121)
    a = rng.uniform(size=(m, n))
    b = rng.uniform(size=(m, n))
    mask_a1 = rng.uniform(size=(m, n)) < 0.2
    mask_a2 = rng.uniform(size=(m, n)) < 0.1
    mask_b1 = rng.uniform(size=(m, n)) < 0.15
    mask_b2 = rng.uniform(size=(m, n)) < 0.15
    mask_a1[2, :] = True

    a_nans = a.copy()
    b_nans = b.copy()
    a_nans[mask_a1 | mask_a2] = np.nan
    b_nans[mask_b1 | mask_b2] = np.nan

    a_masked1 = np.ma.masked_array(a, mask=mask_a1)
    b_masked1 = np.ma.masked_array(b, mask=mask_b1)
    a_masked1[mask_a2] = np.nan
    b_masked1[mask_b2] = np.nan

    a_masked2 = np.ma.masked_array(a, mask=mask_a2)
    b_masked2 = np.ma.masked_array(b, mask=mask_b2)
    a_masked2[mask_a1] = np.nan
    b_masked2[mask_b1] = np.nan

    a_masked3 = np.ma.masked_array(a, mask=(mask_a1 | mask_a2))
    b_masked3 = np.ma.masked_array(b, mask=(mask_b1 | mask_b2))

    with warnings.catch_warnings():
        message = 'invalid value encountered'
        warnings.filterwarnings("ignore", message, RuntimeWarning)
        res = func(a_nans, weights=b_nans, nan_policy="omit", axis=axis)
        res1 = func(a_masked1, weights=b_masked1, nan_policy="omit", axis=axis)
        res2 = func(a_masked2, weights=b_masked2, nan_policy="omit", axis=axis)
        res3 = func(a_masked3, weights=b_masked3, nan_policy="raise", axis=axis)
        res4 = func(a_masked3, weights=b_masked3, nan_policy="propagate", axis=axis)

    np.testing.assert_array_equal(res1, res)
    np.testing.assert_array_equal(res2, res)
    np.testing.assert_array_equal(res3, res)
    np.testing.assert_array_equal(res4, res)

