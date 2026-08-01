
def test_ncx2_tails_pdf():
    # ncx2.pdf does not return nans in extreme tails(example from gh-1577)
    # NB: this is to check that nan_to_num is not needed in ncx2.pdf
    with warnings.catch_warnings():
        warnings.simplefilter('error', RuntimeWarning)
        assert_equal(stats.ncx2.pdf(1, np.arange(340, 350), 2), 0)
        logval = stats.ncx2.logpdf(1, np.arange(340, 350), 2)

    assert_(np.isneginf(logval).all())

    # Verify logpdf has extended precision when pdf underflows to 0
    with warnings.catch_warnings():
        warnings.simplefilter('error', RuntimeWarning)
        assert_equal(stats.ncx2.pdf(10000, 3, 12), 0)
        assert_allclose(stats.ncx2.logpdf(10000, 3, 12), -4662.444377524883)

