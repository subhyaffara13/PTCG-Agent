
def test_issue_17247_expression_blowup_1():
    M = Matrix([[1+x, 1-x], [1-x, 1+x]])
    with dotprodsimp(True):
        assert M.exp().expand() == Matrix([
            [ (exp(2*x) + exp(2))/2, (-exp(2*x) + exp(2))/2],
            [(-exp(2*x) + exp(2))/2,  (exp(2*x) + exp(2))/2]])


def test_issue_17247_expression_blowup_1():
    M = Matrix([[1+x, 1-x], [1-x, 1+x]])
    with dotprodsimp(True):
        assert M.exp().expand() == Matrix([
            [ (exp(2*x) + exp(2))/2, (-exp(2*x) + exp(2))/2],
            [(-exp(2*x) + exp(2))/2,  (exp(2*x) + exp(2))/2]])

