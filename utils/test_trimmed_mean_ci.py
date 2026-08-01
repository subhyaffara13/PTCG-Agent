
def test_trimmed_mean_ci():
    # Tests the confidence intervals of the trimmed mean.
    data = ma.array([545,555,558,572,575,576,578,580,
                     594,605,635,651,653,661,666])
    assert_almost_equal(ms.trimmed_mean(data,0.2), 596.2, 1)
    assert_equal(np.round(ms.trimmed_mean_ci(data,(0.2,0.2)),1),
                 [561.8, 630.6])

