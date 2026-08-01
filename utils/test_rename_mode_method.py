
def test_rename_mode_method(fun, xp):
    rng = np.random.default_rng(23498459284629827814)
    x = xp.asarray(rng.random(10))
    y = xp.asarray(rng.random(10))

    if fun == stats.wilcoxon:
        args = (x,)
    elif fun == stats.ks_1samp:
        args = (x, special.ndtr)
    else:
        args = (x, y)

    res = fun(*args, method='exact')
    res2 = fun(*args, mode='exact')
    xp_assert_equal(res.statistic, res2.statistic)
    xp_assert_equal(res.pvalue, res2.pvalue)

    err = rf"{fun.__name__}\(\) got multiple values for argument"
    with pytest.raises(TypeError, match=err):
        fun(*args, method='exact', mode='exact')

