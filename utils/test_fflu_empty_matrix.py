
def test_fflu_empty_matrix():
    A = DomainMatrix([], (0, 0), ZZ)
    P, L, D, U = A.fflu()
    assert P.shape == (0, 0)
    assert L.shape == (0, 0)
    assert D.shape == (0, 0)
    assert U.shape == (0, 0)

