
def test_ncx2_zero_nc_rvs():
    # gh-5441
    # ncx2 with nc=0 is identical to chi2
    result = stats.ncx2.rvs(df=10, nc=0, random_state=1)
    expected = stats.chi2.rvs(df=10, random_state=1)
    assert_allclose(result, expected, atol=1e-15)

