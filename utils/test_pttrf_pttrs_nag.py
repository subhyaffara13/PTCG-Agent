
def test_pttrf_pttrs_NAG(d, e, d_expect, e_expect, b, x_expect):
    # test to assure that wrapper is consistent with NAG Manual Mark 26
    # example problems: f07jdf and f07jef (real)
    # examples: f07jrf and f07csf (complex)
    # NAG examples provide 4 decimals.
    # (Links expire, so please search for "NAG Library Manual Mark 26" online)

    atol = 1e-4
    pttrf = get_lapack_funcs('pttrf', dtype=e[0])
    _d, _e, info = pttrf(d, e)
    assert_allclose(_d, d_expect, atol=atol)
    assert_allclose(_e, e_expect, atol=atol)

    pttrs = get_lapack_funcs('pttrs', dtype=e[0])
    _x, info = pttrs(_d, _e.conj(), b)
    assert_allclose(_x, x_expect, atol=atol)

    # also test option `lower`
    if e.dtype in COMPLEX_DTYPES:
        _x, info = pttrs(_d, _e, b, lower=1)
        assert_allclose(_x, x_expect, atol=atol)

