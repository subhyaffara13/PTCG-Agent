
def test_issue_17247_expression_blowup_11():
    M = Matrix(6, 6, lambda i, j: 1 + (-1)**(i+j)*I)
    with dotprodsimp(True):
        assert M.cofactor_matrix() == Matrix(6, 6, [0]*36)


def test_issue_17247_expression_blowup_11():
    M = Matrix(6, 6, lambda i, j: 1 + (-1)**(i+j)*I)
    with dotprodsimp(True):
        assert M.cofactor_matrix() == Matrix(6, 6, [0]*36)

