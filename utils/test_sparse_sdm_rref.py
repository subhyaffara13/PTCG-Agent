
def test_sparse_sdm_rref(name, A, A_rref, den):
    A = A.to_field().to_sdm()
    _check_divide(sdm_irref(A)[:2], A_rref, den)

