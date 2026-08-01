
def test_newaxis_get():
    A = coo_array(np.arange(4 * 5 * 6).reshape((4, 5, 6)))
    D = A.toarray()
    assert_equal(A[:5, 3:, 1].toarray(), D[:5, 3:, 1])
    assert_equal(A[None, :5, 1:3, None, 1].toarray(), D[None, :5, 1:3, None, 1])
    assert_equal(A[None, :5, 3:, 1, None].toarray(), D[None, :5, 3:, 1, None])
    assert_equal(A[None, :5, ..., None].toarray(), D[None, :5, ..., None])

