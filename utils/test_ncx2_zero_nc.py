
def test_ncx2_zero_nc(method, expected):
    # gh-5441
    # ncx2 with nc=0 is identical to chi2
    # Comparison to R (v3.5.1)
    # > options(digits=10)
    # > pchisq(0.1, df=10, ncp=c(0,4))
    # > dchisq(0.1, df=10, ncp=c(0,4))
    # > dchisq(0.1, df=10, ncp=c(0,4), log=TRUE)
    # > qchisq(0.1, df=10, ncp=c(0,4))

    result = getattr(stats.ncx2, method)(0.1, nc=[0, 4], df=10)
    assert_allclose(result, expected, atol=1e-15)

