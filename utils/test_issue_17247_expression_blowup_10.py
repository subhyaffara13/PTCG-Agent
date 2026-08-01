
def test_issue_17247_expression_blowup_10():
    M = Matrix(6, 6, lambda i, j: 1 + (-1)**(i+j)*I)
    with dotprodsimp(True):
        assert M.cofactor(0, 0) == 0


def test_issue_17247_expression_blowup_10():
    M = Matrix(6, 6, lambda i, j: 1 + (-1)**(i+j)*I)
    with dotprodsimp(True):
        assert M.cofactor(0, 0) == 0

