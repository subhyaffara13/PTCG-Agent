
def test_issue_19841():
    G1 = GUE('U', 2)
    G2 = G1.xreplace({2: 2})
    assert G1.args == G2.args

    X = MatrixSymbol('X', 2, 2)
    G = GSE('U', 2)
    h_pspace = RandomMatrixPSpace('P', model=density(G))
    H = RandomMatrixSymbol('H', 2, 2, pspace=h_pspace)
    H2 = RandomMatrixSymbol('H', 2, 2, pspace=None)
    assert H.doit() == H

    assert (2*H).xreplace({H: X}) == 2*X
    assert (2*H).xreplace({H2: X}) == 2*H
    assert (2*H2).xreplace({H: X}) == 2*H2
    assert (2*H2).xreplace({H2: X}) == 2*X

