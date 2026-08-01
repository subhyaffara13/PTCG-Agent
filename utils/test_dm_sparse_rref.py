
def test_dm_sparse_rref(name, A, A_rref, den):
    A = A.to_field().to_sparse()
    _check_divide(A.rref(), A_rref, den)

