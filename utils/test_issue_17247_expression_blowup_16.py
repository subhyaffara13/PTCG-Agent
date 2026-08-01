
def test_issue_17247_expression_blowup_16():
    M = Matrix(8, 8, ([1+x, 1-x]*4 + [1-x, 1+x]*4)*4)
    with dotprodsimp(True):
        assert M.columnspace() == [Matrix([[x + 1],[1 - x],[x + 1],[1 - x],[x + 1],[1 - x],[x + 1],[1 - x]]), Matrix([[1 - x],[x + 1],[1 - x],[x + 1],[1 - x],[x + 1],[1 - x],[x + 1]])]


def test_issue_17247_expression_blowup_16():
    M = Matrix(8, 8, ([1+x, 1-x]*4 + [1-x, 1+x]*4)*4)
    with dotprodsimp(True):
        assert M.columnspace() == [Matrix([[x + 1],[1 - x],[x + 1],[1 - x],[x + 1],[1 - x],[x + 1],[1 - x]]), Matrix([[1 - x],[x + 1],[1 - x],[x + 1],[1 - x],[x + 1],[1 - x],[x + 1]])]

