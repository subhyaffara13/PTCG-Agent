
def test_issue_17247_expression_blowup_8():
    M = Matrix(8, 8, [x+i for i in range (64)])
    with dotprodsimp(True):
        assert M.det('lu') == 0


def test_issue_17247_expression_blowup_8():
    M = Matrix(8, 8, [x+i for i in range (64)])
    with dotprodsimp(True):
        assert M.det('lu') == 0

