
def test_2d_coo_get():
    B = coo_array(np.arange(4 * 5).reshape((4, 5)))

    assert B[0, 0] == 0
    assert B[3, 4] == 19

    assert_equal(B[1:3, 0].toarray(), B.toarray()[1:3, 0])
    assert_equal(B[2, 1:3].toarray(), B.toarray()[2, 1:3])
    assert_equal(B[:2, 1:5:3].toarray(), B.toarray()[:2, 1:5:3])

    assert_equal(B[[1, 3], 0].toarray(), B.toarray()[[1,3], 0])
    assert_equal(B[2:, [1, 3]].toarray(), B.toarray()[2:, [1,3]])
    assert_equal(B[np.array([1, 3]), 0].toarray(), B.toarray()[[1,3], 0])
    assert_equal(B[2:, np.array([1, 3])].toarray(), B.toarray()[2:, [1,3]])

    assert_equal(B[:, 0].toarray(), B.toarray()[:, 0])
    assert_equal(B[0, :].toarray(), B.toarray()[0, :])

