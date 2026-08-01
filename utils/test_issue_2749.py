
def test_issue_2749():
    A = MatrixSymbol("A", 5, 2)
    assert (A.T * A).I.as_explicit() == Matrix([[(A.T * A).I[0, 0], (A.T * A).I[0, 1]], \
    [(A.T * A).I[1, 0], (A.T * A).I[1, 1]]])

