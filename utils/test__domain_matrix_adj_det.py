
def test_DomainMatrix_adj_det():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    adjA = DomainMatrix([[ZZ(4), ZZ(-2)], [ZZ(-3), ZZ(1)]], (2, 2), ZZ)
    assert A.adj_det() == (adjA, ZZ(-2))

