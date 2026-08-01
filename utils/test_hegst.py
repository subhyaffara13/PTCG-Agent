
def test_hegst():
    rng = np.random.default_rng(1234)
    for ind, dtype in enumerate(COMPLEX_DTYPES):
        # DTYPES = <c,z> hegst
        n = 10

        potrf, hegst, heevd, hegvd = get_lapack_funcs(('potrf', 'hegst',
                                                       'heevd', 'hegvd'),
                                                      dtype=dtype)

        A = rng.random((n, n)).astype(dtype) + 1j * rng.random((n, n)).astype(dtype)
        A = (A + A.conj().T)/2
        # B must be positive definite
        B = rng.random((n, n)).astype(dtype) + 1j * rng.random((n, n)).astype(dtype)
        B = (B + B.conj().T)/2 + 2 * np.eye(n, dtype=dtype)

        # Perform eig (hegvd)
        eig_gvd, _, info = hegvd(A, B)
        assert_(info == 0)

        # Convert to std problem potrf
        b, info = potrf(B)
        assert_(info == 0)
        a, info = hegst(A, b)
        assert_(info == 0)

        eig, _, info = heevd(a)
        assert_(info == 0)
        assert_allclose(eig, eig_gvd, rtol=1e-4)

