
def test_gtsvx_NAG(du, d, dl, b, x):
    # Test to ensure wrapper is consistent with NAG Manual Mark 26
    # example problems: real (f07cbf) and complex (f07cpf)
    gtsvx = get_lapack_funcs('gtsvx', dtype=d.dtype)

    gtsvx_out = gtsvx(dl, d, du, b)
    dlf, df, duf, du2f, ipiv, x_soln, rcond, ferr, berr, info = gtsvx_out

    assert_array_almost_equal(x, x_soln)

