
def test_ncx2_gh11777():
    # regression test for gh-11777:
    # At high values of degrees of freedom df, ensure the pdf of ncx2 does
    # not get clipped to zero when the non-centrality parameter is
    # sufficiently less than df
    df = 6700
    nc = 5300
    x = np.linspace(stats.ncx2.ppf(0.001, df, nc),
                    stats.ncx2.ppf(0.999, df, nc), num=10000)
    ncx2_pdf = stats.ncx2.pdf(x, df, nc)
    gauss_approx = stats.norm.pdf(x, df + nc, np.sqrt(2 * df + 4 * nc))
    # use huge tolerance as we're only looking for obvious discrepancy
    assert_allclose(ncx2_pdf, gauss_approx, atol=1e-4)

