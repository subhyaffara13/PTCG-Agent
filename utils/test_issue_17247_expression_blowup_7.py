
def test_issue_17247_expression_blowup_7():
    M = Matrix(6, 6, lambda i, j: 1 + (-1)**(i+j)*I)
    with dotprodsimp(True):
        assert M.det('berkowitz') == 0


def test_issue_17247_expression_blowup_7():
    M = Matrix(6, 6, lambda i, j: 1 + (-1)**(i+j)*I)
    with dotprodsimp(True):
        assert M.det('berkowitz') == 0

