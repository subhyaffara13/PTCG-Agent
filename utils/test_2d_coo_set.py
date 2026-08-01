
def test_2d_coo_set(A, D, idx):
    D[idx] = A[idx] = -D[idx]
    assert_equal(A.toarray(), D)

