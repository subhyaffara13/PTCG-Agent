
def test_Matrix_rref(name, A, A_rref, den):
    K = A.domain
    A = A.to_Matrix()
    A_rref_found, pivots = A.rref()
    if K.is_EX:
        A_rref_found = A_rref_found.expand()
    _check_divide((A_rref_found, pivots), A_rref, den)

