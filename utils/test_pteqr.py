
def test_pteqr(dtype, realtype, compute_z):
    '''
    Tests the ?pteqr lapack routine for all dtypes and compute_z parameters.
    It generates random SPD matrix diagonals d and e, and then confirms
    correct eigenvalues with scipy.linalg.eig. With applicable compute_z=2 it
    tests that z can reform A.
    '''
    atol = 1000*np.finfo(dtype).eps
    pteqr = get_lapack_funcs(('pteqr'), dtype=dtype)

    n = 10

    d, e, A, z = pteqr_get_d_e_A_z(dtype, realtype, n, compute_z)

    d_pteqr, e_pteqr, z_pteqr, info = pteqr(d=d, e=e, z=z, compute_z=compute_z)
    assert_equal(info, 0, f"info = {info}, should be 0.")

    # compare the routine's eigenvalues with scipy.linalg.eig's.
    assert_allclose(np.sort(eigh(A)[0]), np.sort(d_pteqr), atol=atol)

    if compute_z:
        # verify z_pteqr as orthogonal
        assert_allclose(z_pteqr @ np.conj(z_pteqr).T, np.identity(n),
                        atol=atol)
        # verify that z_pteqr recombines to A
        assert_allclose(z_pteqr @ np.diag(d_pteqr) @ np.conj(z_pteqr).T,
                        A, atol=atol)

