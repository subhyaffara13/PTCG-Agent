
def test_ncx2_tails_ticket_955():
    # Trac #955 -- check that the cdf computed by special functions
    # matches the integrated pdf
    a = stats.ncx2.cdf(np.arange(20, 25, 0.2), 2, 1.07458615e+02)
    b = stats.ncx2._cdfvec(np.arange(20, 25, 0.2), 2, 1.07458615e+02)
    assert_allclose(a, b, rtol=1e-3, atol=0)

