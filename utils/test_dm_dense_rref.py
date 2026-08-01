
def test_dm_dense_rref(name, A, A_rref, den):
    A = A.to_field()
    _check_divide(A.rref(), A_rref, den)

