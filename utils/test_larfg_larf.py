
def test_larfg_larf():
    rng = np.random.default_rng(1234)
    a0 = rng.random((4, 4))
    a0 = a0.T.dot(a0)

    a0j = rng.random((4, 4)) + 1j*rng.random((4, 4))
    a0j = a0j.T.conj().dot(a0j)

    # our test here will be to do one step of reducing a hermetian matrix to
    # tridiagonal form using householder transforms.

    for dtype in 'fdFD':
        larfg, larf = get_lapack_funcs(['larfg', 'larf'], dtype=dtype)

        if dtype in 'FD':
            a = a0j.copy()
        else:
            a = a0.copy()

        # generate a householder transform to clear a[2:,0]
        alpha, x, tau = larfg(a.shape[0]-1, a[1, 0], a[2:, 0])

        # create expected output
        expected = np.zeros_like(a[:, 0])
        expected[0] = a[0, 0]
        expected[1] = alpha

        # assemble householder vector
        v = np.zeros_like(a[1:, 0])
        v[0] = 1.0
        v[1:] = x

        # apply transform from the left
        a[1:, :] = larf(v, tau.conjugate(), a[1:, :], np.zeros(a.shape[1]))

        # apply transform from the right
        a[:, 1:] = larf(v, tau, a[:, 1:], np.zeros(a.shape[0]), side='R')

        assert_allclose(a[:, 0], expected, atol=1e-5)
        assert_allclose(a[0, :], expected, atol=1e-5)

