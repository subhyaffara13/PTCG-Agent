
def test_masked_stat_1d():
    # basic test of _axis_nan_policy_factory with 1D masked sample
    males = [19, 22, 16, 29, 24]
    females = [20, 11, 17, 12]
    res = stats.mannwhitneyu(males, females)

    # same result when extra nan is omitted
    females2 = [20, 11, 17, np.nan, 12]
    res2 = stats.mannwhitneyu(males, females2, nan_policy='omit')
    np.testing.assert_array_equal(res2, res)

    # same result when extra element is masked
    females3 = [20, 11, 17, 1000, 12]
    mask3 = [False, False, False, True, False]
    females3 = np.ma.masked_array(females3, mask=mask3)
    res3 = stats.mannwhitneyu(males, females3)
    np.testing.assert_array_equal(res3, res)

    # same result when extra nan is omitted and additional element is masked
    females4 = [20, 11, 17, np.nan, 1000, 12]
    mask4 = [False, False, False, False, True, False]
    females4 = np.ma.masked_array(females4, mask=mask4)
    res4 = stats.mannwhitneyu(males, females4, nan_policy='omit')
    np.testing.assert_array_equal(res4, res)

    # same result when extra elements, including nan, are masked
    females5 = [20, 11, 17, np.nan, 1000, 12]
    mask5 = [False, False, False, True, True, False]
    females5 = np.ma.masked_array(females5, mask=mask5)
    res5 = stats.mannwhitneyu(males, females5, nan_policy='propagate')
    res6 = stats.mannwhitneyu(males, females5, nan_policy='raise')
    np.testing.assert_array_equal(res5, res)
    np.testing.assert_array_equal(res6, res)

