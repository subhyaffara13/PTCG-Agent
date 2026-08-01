
def test_cse_MatrixExpr():
    A = MatrixSymbol('A', 3, 3)
    y = MatrixSymbol('y', 3, 1)

    expr1 = (A.T*A).I * A * y
    expr2 = (A.T*A) * A * y
    replacements, reduced_exprs = cse([expr1, expr2])
    assert len(replacements) > 0

    replacements, reduced_exprs = cse([expr1 + expr2, expr1])
    assert replacements

    replacements, reduced_exprs = cse([A**2, A + A**2])
    assert replacements

