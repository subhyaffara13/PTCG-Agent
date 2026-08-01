
def test_ncx2_gh12731():
    # test that gh-12731 is resolved; previously these were all 0.5
    nc = 10**np.arange(5, 10)
    assert_equal(stats.ncx2.cdf(1e4, df=1, nc=nc), 0)

