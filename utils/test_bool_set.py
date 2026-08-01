
def test_bool_set():
    D_orig = np.arange(4 * 6 * 6 * 3 * 4).reshape((4, 6, 6, 3, 4))
    A_orig = coo_array(D_orig)

    A, D = A_orig.copy(), D_orig.copy()
    D[D > 500] = A[A > 500] = -33
    assert_equal(A.toarray(), D)

    A, D = A_orig.copy(), D_orig.copy()
    D[D > 500] = A[A > 500] = -77
    assert_equal(A.toarray(), D)

    A, D = A_orig.copy(), D_orig.copy()
    bool0 = A[:, 0, 0, 0, 0] > 50
    idx = (bool0, slice(2, 3, None), [1], slice(None, 2, 2), bool0)
    idxnp = (bool0.toarray(), slice(2, 3, 1), [1], slice(0, 2, 2), bool0.toarray())

    D[idxnp] = A[idx] = -55
    assert_equal(A.toarray(), D)

    A, D = A_orig.copy(), D_orig.copy()
    D[idxnp] = A[idxnp] = -88
    assert_equal(A.toarray(), D)

