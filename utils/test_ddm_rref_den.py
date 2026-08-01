
def test_ddm_rref_den(name, A, A_rref, den):
    A = A.to_ddm()
    _check_cancel(A.rref_den(), A_rref, den)

