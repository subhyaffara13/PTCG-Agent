
def test_cse_MatrixSymbol():
    # MatrixSymbols have non-Basic args, so make sure that works
    A = MatrixSymbol("A", 3, 3)
    assert cse(A) == ([], [A])

    n = symbols('n', integer=True)
    B = MatrixSymbol("B", n, n)
    assert cse(B) == ([], [B])

    assert cse(A[0] * A[0]) == ([], [A[0]*A[0]])

    assert cse(A[0,0]*A[0,1] + A[0,0]*A[0,1]*A[0,2]) == ([(x0, A[0, 0]*A[0, 1])], [x0*A[0, 2] + x0])

