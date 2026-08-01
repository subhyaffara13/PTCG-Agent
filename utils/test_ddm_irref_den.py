
def test_ddm_irref_den(name, A, A_rref, den):
    A = A.to_ddm().copy()
    (den_found, pivots_found) = ddm_irref_den(A, A.domain)
    result = (A, den_found, pivots_found)
    _check_cancel(result, A_rref, den)

