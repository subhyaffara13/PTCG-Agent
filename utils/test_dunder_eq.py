
def test_dunder_eq(A, Asp):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", sp.sparse.SparseEfficiencyWarning)
        assert (Asp == Asp).toarray().all()
        assert (A == Asp).all()

