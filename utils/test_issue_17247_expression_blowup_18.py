
def test_issue_17247_expression_blowup_18():
    M = Matrix(6, 6, ([1+x, 1-x]*3 + [1-x, 1+x]*3)*3)
    with dotprodsimp(True):
        assert not M.is_nilpotent()


def test_issue_17247_expression_blowup_18():
    M = Matrix(6, 6, ([1+x, 1-x]*3 + [1-x, 1+x]*3)*3)
    with dotprodsimp(True):
        assert not M.is_nilpotent()

