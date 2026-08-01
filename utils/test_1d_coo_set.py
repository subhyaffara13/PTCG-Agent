
def test_1d_coo_set():
    D = np.arange(9)
    A = coo_array(D)

    A[0] = D[0] = -1
    assert_equal(A.toarray(), D)
    A[4] = D[4] = -2
    assert_equal(A.toarray(), D)

    A[1:3] = D[1:3] = [-2, -3]
    assert_equal(A.toarray(), D)
    A[:3] = D[:3] = [-7, -8, -9]
    assert_equal(A.toarray(), D)
    A[1:] = D[1:] = -D[1:]
    assert_equal(A.toarray(), D)
    A[1:5:2] = D[1:5:2] = -D[1:5:2]
    assert_equal(A.toarray(), D)

    A[[1, 3, 4]] = D[[1, 3, 4]] = -D[[1, 3, 4]]
    assert_equal(A.toarray(), D)
    A[[3, 4, 1]] = D[[3, 4, 1]] = -D[[1, 2, 3]]
    assert_equal(A.toarray(), D)

