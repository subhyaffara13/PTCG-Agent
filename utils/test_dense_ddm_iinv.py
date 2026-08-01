
def test_dense_ddm_iinv(name, A, A_inv, den):
    A = A.to_field().to_ddm().copy()
    K = A.domain
    A_result = A.copy()
    if den != 0:
        A_inv = (A_inv.to_field() / den).to_ddm()
        ddm_iinv(A_result, A, K)
        assert A_result == A_inv
    else:
        raises(DMNonInvertibleMatrixError, lambda: ddm_iinv(A_result, A, K))

