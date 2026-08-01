
def test_ncf_edge_case(df1, df2, x):
    # Test for edge case described in gh-11660.
    # Non-central Fisher distribution when nc = 0
    # should be the same as Fisher distribution.
    nc = 0
    expected_cdf = stats.f.cdf(x, df1, df2)
    calculated_cdf = stats.ncf.cdf(x, df1, df2, nc)
    assert_allclose(expected_cdf, calculated_cdf, rtol=1e-14)

    # when ncf_gen._skip_pdf will be used instead of generic pdf,
    # this additional test will be useful.
    expected_pdf = stats.f.pdf(x, df1, df2)
    calculated_pdf = stats.ncf.pdf(x, df1, df2, nc)
    assert_allclose(expected_pdf, calculated_pdf, rtol=1e-6)

