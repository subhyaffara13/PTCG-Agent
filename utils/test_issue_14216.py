
def test_issue_14216():
    from sympy.functions.elementary.complexes import unpolarify
    A = MatrixSymbol("A", 2, 2)
    assert unpolarify(A[0, 0]) == A[0, 0]
    assert unpolarify(A[0, 0]*A[1, 0]) == A[0, 0]*A[1, 0]

