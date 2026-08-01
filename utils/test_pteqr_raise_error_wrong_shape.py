
def test_pteqr_raise_error_wrong_shape(dtype, realtype, compute_z):
    pteqr = get_lapack_funcs(('pteqr'), dtype=dtype)
    n = 10
    d, e, A, z = pteqr_get_d_e_A_z(dtype, realtype, n, compute_z)
    # test with incorrect/incompatible array sizes
    assert_raises(ValueError, pteqr, d[:-1], e, z=z, compute_z=compute_z)
    assert_raises(ValueError, pteqr, d, e[:-1], z=z, compute_z=compute_z)
    if compute_z:
        assert_raises(ValueError, pteqr, d, e, z=z[:-1], compute_z=compute_z)

