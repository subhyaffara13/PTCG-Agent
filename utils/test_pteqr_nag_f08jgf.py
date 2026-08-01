
def test_pteqr_NAG_f08jgf(compute_z, d, e, d_expect, z_expect):
    '''
    Implements real (f08jgf) example from NAG Manual Mark 26.
    Tests for correct outputs.
    '''
    # the NAG manual has 4 decimals accuracy
    atol = 1e-4
    pteqr = get_lapack_funcs(('pteqr'), dtype=d.dtype)

    z = np.diag(d) + np.diag(e, 1) + np.diag(e, -1)
    _d, _e, _z, info = pteqr(d=d, e=e, z=z, compute_z=compute_z)
    assert_allclose(_d, d_expect, atol=atol)
    assert_allclose(np.abs(_z), np.abs(z_expect), atol=atol)

