
def test_3d_coo_set(A, D, idx):
    D[idx] = A[idx] = -99
    assert_equal(A.toarray(), D)

