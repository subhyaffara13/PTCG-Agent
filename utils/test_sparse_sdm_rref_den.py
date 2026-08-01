
def test_sparse_sdm_rref_den(name, A, A_rref, den):
    A = A.to_sdm().copy()
    K = A.domain
    _check_cancel(sdm_rref_den(A, K), A_rref, den)

