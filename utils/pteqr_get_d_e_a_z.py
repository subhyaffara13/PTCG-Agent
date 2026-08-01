
def pteqr_get_d_e_A_z(dtype, realtype, n, compute_z):
    # used by ?pteqr tests to build parameters
    # returns tuple of (d, e, A, z)
    rng = np.random.RandomState(42)
    if compute_z == 1:
        # build Hermitian A from Q**T * tri * Q = A by creating Q and tri
        A_eig = generate_random_dtype_array((n, n), dtype, rng)
        A_eig = A_eig + np.diag(np.zeros(n) + 4*n)
        A_eig = (A_eig + A_eig.conj().T) / 2
        # obtain right eigenvectors (orthogonal)
        vr = eigh(A_eig)[1]
        # create tridiagonal matrix
        d = generate_random_dtype_array((n,), realtype, rng) + 4
        e = generate_random_dtype_array((n-1,), realtype, rng)
        tri = np.diag(d) + np.diag(e, 1) + np.diag(e, -1)
        # Build A using these factors that sytrd would: (Q**T * tri * Q = A)
        A = vr @ tri @ vr.conj().T
        # vr is orthogonal
        z = vr

    else:
        # d and e are always real per lapack docs.
        d = generate_random_dtype_array((n,), realtype, rng)
        e = generate_random_dtype_array((n-1,), realtype, rng)

        # make SPD
        d = d + 4
        A = np.diag(d) + np.diag(e, 1) + np.diag(e, -1)
        z = np.diag(d) + np.diag(e, -1) + np.diag(e, 1)
    return (d, e, A, z)

