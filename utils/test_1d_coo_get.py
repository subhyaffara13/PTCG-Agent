
def test_1d_coo_get():
    B = coo_array(np.arange(9))

    assert B[0] == 0
    assert B[4] == 4

    assert_equal(B[1:3].toarray(), B.toarray()[1:3])
    assert_equal(B[:3].toarray(), B.toarray()[:3])
    assert_equal(B[1:].toarray(), B.toarray()[1:])
    assert_equal(B[1:5:2].toarray(), B.toarray()[1:5:2])

    assert_equal(B[[1, 3, 4]].toarray(), B.toarray()[[1, 3, 4]])
    assert_equal(B[[3, 4, 1]].toarray(), B.toarray()[[3, 4, 1]])

