
def test_dm_dense_rref_den(name, A, A_rref, den):
    _check_cancel(A.rref_den(), A_rref, den)

