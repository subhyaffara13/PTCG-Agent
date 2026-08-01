
def test_fflu_rank_deficient():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(2), ZZ(4)]], (2, 2), ZZ)
    P, L, D, U = A.fflu()
    assert P.shape == (2, 2)
    assert L.shape == (2, 2)
    assert D.shape == (2, 2)
    assert U.shape == (2, 2)
    assert U.getitem_sympy(1, 1) == 0

