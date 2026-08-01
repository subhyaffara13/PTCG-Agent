
def test_mixed_mask_nan_2():
    # targeted test of _axis_nan_policy_factory with 2D masked sample:
    # check for expected interaction between masks and nans

    # Cases here are
    # [mixed nan/mask, all nans, all masked,
    # unmasked nan, masked nan, unmasked non-nan]
    a = [[1, np.nan, 2], [np.nan, np.nan, np.nan], [1, 2, 3],
         [1, np.nan, 3], [1, np.nan, 3], [1, 2, 3]]
    mask = [[1, 0, 1], [0, 0, 0], [1, 1, 1],
            [0, 0, 0], [0, 1, 0], [0, 0, 0]]
    a_masked = np.ma.masked_array(a, mask=mask)
    b = [[4, 5, 6]]
    ref1 = stats.ranksums([1, 3], [4, 5, 6])
    ref2 = stats.ranksums([1, 2, 3], [4, 5, 6])

    # nan_policy = 'omit'
    # all elements are removed from first three rows
    # middle element is removed from fourth and fifth rows
    # no elements removed from last row
    res = stats.ranksums(a_masked, b, nan_policy='omit', axis=-1)
    stat_ref = [np.nan, np.nan, np.nan,
                ref1.statistic, ref1.statistic, ref2.statistic]
    p_ref = [np.nan, np.nan, np.nan,
             ref1.pvalue, ref1.pvalue, ref2.pvalue]
    np.testing.assert_array_equal(res.statistic, stat_ref)
    np.testing.assert_array_equal(res.pvalue, p_ref)

    # nan_policy = 'propagate'
    # nans propagate in first, second, and fourth row
    # all elements are removed by mask from third row
    # middle element is removed from fifth row
    # no elements removed from last row
    res = stats.ranksums(a_masked, b, nan_policy='propagate', axis=-1)
    stat_ref = [np.nan, np.nan, np.nan,
                np.nan, ref1.statistic, ref2.statistic]
    p_ref = [np.nan, np.nan, np.nan,
             np.nan, ref1.pvalue, ref2.pvalue]
    np.testing.assert_array_equal(res.statistic, stat_ref)
    np.testing.assert_array_equal(res.pvalue, p_ref)

