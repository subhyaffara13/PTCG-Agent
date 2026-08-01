
def test_5d_coo_set(A, D, ix, msg):
    D[ix] = A[ix] = -99
    assert_equal(A.toarray(), D, err_msg=f"\nTest of: {msg}\n")

