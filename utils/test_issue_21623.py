
def test_issue_21623():
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    M = MatrixSymbol('X', 2, 2)
    assert gcd_terms(M[0,0], 1) == M[0,0]

