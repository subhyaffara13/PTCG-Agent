
def test_expm(B):
    if B.__class__.__name__[:3] != 'csc':
        return

    Bmat = scipy.sparse.csc_matrix(B)

    C = spla.expm(B)

    assert isinstance(C, scipy.sparse.sparray)
    npt.assert_allclose(
        C.todense(),
        spla.expm(Bmat).todense()
    )


def test_expm(matrices):
    A_dense, A_sparse, b = matrices
    x0 = splin.expm(sp.csc_array(A_dense))
    x = splin.expm(A_sparse)
    assert_allclose(x.todense(), x0.todense())

