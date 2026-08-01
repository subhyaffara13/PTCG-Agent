
def test_dm_sparse_rref_den(name, A, A_rref, den):
    A = A.to_sparse()
    _check_cancel(A.rref_den(), A_rref, den)

