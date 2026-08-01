
def test_sdm_rref_den(name, A, A_rref, den):
    A = A.to_sdm()
    _check_cancel(A.rref_den(), A_rref, den)

