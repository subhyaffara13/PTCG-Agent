
def test_gttrf_gttrs_NAG_f07cdf_f07cef_f07crf_f07csf(du, d, dl, du_exp, d_exp,
                                                     du2_exp, ipiv_exp, b, x):
    # test to assure that wrapper is consistent with NAG Library Manual Mark 26
    # example problems: f07cdf and f07cef (real)
    # examples: f07crf and f07csf (complex)
    # (Links may expire, so search for "NAG Library Manual Mark 26" online)

    gttrf, gttrs = get_lapack_funcs(('gttrf', "gttrs"), (du[0], du[0]))

    _dl, _d, _du, du2, ipiv, info = gttrf(dl, d, du)
    assert_allclose(du2, du2_exp)
    assert_allclose(_du, du_exp)
    assert_allclose(_d, d_exp, atol=1e-4)  # NAG examples provide 4 decimals.
    assert_allclose(ipiv, ipiv_exp)

    x_gttrs, info = gttrs(_dl, _d, _du, du2, ipiv, b)

    assert_allclose(x_gttrs, x)

