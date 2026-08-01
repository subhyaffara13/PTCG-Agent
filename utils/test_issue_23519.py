
def test_issue_23519():
    N = Symbol("N", integer=True)
    M1 = MatrixSymbol("M1", N, N)
    M2 = MatrixSymbol("M2", N, N)
    I = Identity(N)
    z = (M2 + 2 * (M2 + I) * M1 + I)
    assert z.coeff(M1) == 2*I + 2*M2

