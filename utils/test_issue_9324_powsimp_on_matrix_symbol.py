
def test_issue_9324_powsimp_on_matrix_symbol():
    M = MatrixSymbol('M', 10, 10)
    expr = powsimp(M, deep=True)
    assert expr == M
    assert expr.args[0] == Str('M')

