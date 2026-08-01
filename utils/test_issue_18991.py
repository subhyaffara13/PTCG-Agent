
def test_issue_18991():
    A = MatrixSymbol('A', 2, 2)
    assert signsimp(-A * A - A) == -A * A - A

