
def test_dm_sparse_rref_den_keep_domain_CD(name, A, A_rref, den):
    A = A.to_sparse()
    A_rref_f, den_f, pivots_f = A.rref_den(keep_domain=False, method='CD')
    A_rref_f = A_rref_f.to_field() / den_f
    _check_divide((A_rref_f, pivots_f), A_rref, den)

