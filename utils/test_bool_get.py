
def test_bool_get():
    D = np.arange(4 * 6 * 6 * 3 * 4).reshape((4, 6, 6, 3, 4))
    A = coo_array(D)

    assert_equal(A[D > 500].toarray(), D[D > 500])
    assert_equal(A[D > 5000].toarray(), D[D > 5000])
    assert_equal(A[D > -1].toarray(), D[D > -1])

    assert_equal(A[A > 500].toarray(), D[D > 500])
    assert_equal(A[A > 5000].toarray(), D[D > 5000])
    assert_equal(A[A < -1].toarray(), D[D < -1])

    bi0 = A[:, 0, 0, 0, 0] > 50
    bi1 = A[0, :, 0, 0, 0] > 50

    idx = (bi0, slice(2, 3, None), [1], slice(None, 2, 2), bi0)
    idxnp = (bi0.toarray(), slice(2, 3, 1), [1], slice(0, 2, 2), bi0.toarray())
    result = D[idxnp]
    assert_equal(A[idx].toarray(), result)
    assert_equal(A[idxnp].toarray(), result)

    idx = (slice(2, 3, None), bi1, bi1, slice(None, 2, 2), [1])
    idxnp = (slice(2, 3, None), bi1.toarray(), bi1.toarray(), slice(None, 2, 2), [1])
    result = D[idxnp]
    assert_equal(A[idx].toarray(), result)

