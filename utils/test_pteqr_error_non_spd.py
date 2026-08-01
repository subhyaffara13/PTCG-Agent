
def test_pteqr_error_non_spd(dtype, realtype, compute_z):
    pteqr = get_lapack_funcs(('pteqr'), dtype=dtype)

    n = 10
    d, e, A, z = pteqr_get_d_e_A_z(dtype, realtype, n, compute_z)

    # test with non-spd matrix
    d_pteqr, e_pteqr, z_pteqr, info = pteqr(d - 4, e, z=z, compute_z=compute_z)
    assert info > 0

