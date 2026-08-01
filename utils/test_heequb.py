
def test_heequb():
    # zheequb has a bug for versions =< LAPACK 3.9.0
    # See Reference-LAPACK gh-61 and gh-408
    # Hence the zheequb test is customized accordingly to avoid
    # work scaling.
    A = np.diag([2]*5 + [1002]*5) + np.diag(np.ones(9), k=1)*1j
    s, scond, amax, info = lapack.zheequb(A)
    assert_equal(info, 0)
    assert_allclose(np.log2(s), [0., -1.]*2 + [0.] + [-4]*5)

    A = np.diag(2**np.abs(np.arange(-5, 6)) + 0j)
    A[5, 5] = 1024
    A[5, 0] = 16j
    s, scond, amax, info = lapack.cheequb(A.astype(np.complex64), lower=1)
    assert_equal(info, 0)
    assert_allclose(np.log2(s), [-2, -1, -1, 0, 0, -5, 0, -1, -1, -2, -2])

