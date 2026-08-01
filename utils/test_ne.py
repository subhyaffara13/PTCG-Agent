
def test_ne(same_matrix):
    sp_sparse, pd_sparse = same_matrix
    # temporary splint until pydata sparse support sparray equality
    sp_sparse = sp.coo_matrix(sp_sparse).asformat(sp_sparse.format)
    assert not (sp_sparse != pd_sparse).any()

