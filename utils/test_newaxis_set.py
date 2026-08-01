
def test_newaxis_set():
    D = np.arange(4 * 5 * 6).reshape((4, 5, 6))
    A = coo_array(D)

    A[None, 3:, 1] = D[None, 3:, 1] = 5
    assert_equal(A.toarray(), D)
    A[3:, 1, None] = D[3:, 1, None] = 7
    assert_equal(A.toarray(), D)
    A[3:, None, 1] = D[3:, None, 1] = 3
    assert_equal(A.toarray(), D)

