
def test_3d_coo_get():
    A = coo_array(np.arange(4 * 5 * 6).reshape((4, 5, 6)))
    assert A[0, 0, 0] == 0
    assert A[3, 4, 5] == 119

    assert_equal(A[0, 1:3, 0].toarray(), A.toarray()[0, 1:3, 0])
    assert_equal(A[0, 1:3, 3].toarray(), A.toarray()[0, 1:3, 3])
    assert_equal(A[:3, 1:5:2, 2:].toarray(), A.toarray()[:3, 1:5:2, 2:])

    assert_equal(A[[1, 3], 0, 0].toarray(), A.toarray()[[1, 3], 0, 0])
    assert_equal(A[:2, 1:3, [1, 3]].toarray(), A.toarray()[:2, 1:3, [1, 3]])

    assert_equal(A[0, :, 0].toarray(), A.toarray()[0, :, 0])
    assert_equal(A[:, :, 0].toarray(), A.toarray()[:, :, 0])

