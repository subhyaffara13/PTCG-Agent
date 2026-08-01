
def test_issue_17247_expression_blowup_17():
    M = Matrix(8, 8, [x+i for i in range (64)])
    with dotprodsimp(True):
        assert M.nullspace() == [
            Matrix([[1],[-2],[1],[0],[0],[0],[0],[0]]),
            Matrix([[2],[-3],[0],[1],[0],[0],[0],[0]]),
            Matrix([[3],[-4],[0],[0],[1],[0],[0],[0]]),
            Matrix([[4],[-5],[0],[0],[0],[1],[0],[0]]),
            Matrix([[5],[-6],[0],[0],[0],[0],[1],[0]]),
            Matrix([[6],[-7],[0],[0],[0],[0],[0],[1]])]


def test_issue_17247_expression_blowup_17():
    M = Matrix(8, 8, [x+i for i in range (64)])
    with dotprodsimp(True):
        assert M.nullspace() == [
            Matrix([[1],[-2],[1],[0],[0],[0],[0],[0]]),
            Matrix([[2],[-3],[0],[1],[0],[0],[0],[0]]),
            Matrix([[3],[-4],[0],[0],[1],[0],[0],[0]]),
            Matrix([[4],[-5],[0],[0],[0],[1],[0],[0]]),
            Matrix([[5],[-6],[0],[0],[0],[0],[1],[0]]),
            Matrix([[6],[-7],[0],[0],[0],[0],[0],[1]])]

