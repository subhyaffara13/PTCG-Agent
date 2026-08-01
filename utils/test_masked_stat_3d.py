
def test_masked_stat_3d(axis):
    # basic test of _axis_nan_policy_factory with 3D masked sample
    rng = np.random.default_rng(3679428403)
    a = rng.random((3, 4, 5))
    b = rng.random((4, 5))
    c = rng.random((4, 1))

    mask_a = a < 0.1
    mask_c = [False, False, False, True]
    a_masked = np.ma.masked_array(a, mask=mask_a)
    c_masked = np.ma.masked_array(c, mask=mask_c)

    a_nans = a.copy()
    a_nans[mask_a] = np.nan
    c_nans = c.copy()
    c_nans[mask_c] = np.nan

    res = stats.kruskal(a_nans, b, c_nans, nan_policy='omit', axis=axis)
    res2 = stats.kruskal(a_masked, b, c_masked, axis=axis)
    np.testing.assert_array_equal(res, res2)

