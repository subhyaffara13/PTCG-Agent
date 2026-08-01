
def test_issue_17247_expression_blowup_6():
    M = Matrix(8, 8, [x+i for i in range (64)])
    with dotprodsimp(True):
        assert M.det('bareiss') == 0


def test_issue_17247_expression_blowup_6():
    M = Matrix(8, 8, [x+i for i in range (64)])
    with dotprodsimp(True):
        assert M.det('bareiss') == 0

