
def test_DomainMatrix_scc():
    Ad = DomainMatrix([[ZZ(1), ZZ(2), ZZ(3)],
                       [ZZ(0), ZZ(1), ZZ(0)],
                       [ZZ(2), ZZ(0), ZZ(4)]], (3, 3), ZZ)
    As = Ad.to_sparse()
    Addm = Ad.rep
    Asdm = As.rep
    for A in [Ad, As, Addm, Asdm]:
        assert Ad.scc() == [[1], [0, 2]]

    A = DM([[ZZ(1), ZZ(2), ZZ(3)]], ZZ)
    raises(DMNonSquareMatrixError, lambda: A.scc())

