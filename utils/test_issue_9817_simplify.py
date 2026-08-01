
def test_issue_9817_simplify():
    # simplify on trace of substituted explicit quadratic form of matrix
    # expressions (a scalar) should return without errors (AttributeError)
    # See issue #9817 and #9190 for the original bug more discussion on this
    from sympy.matrices.expressions import Identity, trace
    v = MatrixSymbol('v', 3, 1)
    A = MatrixSymbol('A', 3, 3)
    x = Matrix([i + 1 for i in range(3)])
    X = Identity(3)
    quadratic = v.T * A * v
    assert simplify((trace(quadratic.as_explicit())).xreplace({v:x, A:X})) == 14

