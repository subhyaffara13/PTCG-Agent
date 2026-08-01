
def test_issue_17247_expression_blowup_5():
    M = Matrix(6, 6, lambda i, j: 1 + (-1)**(i+j)*I)
    with dotprodsimp(True):
        assert M.charpoly('x') == PurePoly(x**6 + (-6 - 6*I)*x**5 + 36*I*x**4, x, domain='EX')


def test_issue_17247_expression_blowup_5():
    M = Matrix(6, 6, lambda i, j: 1 + (-1)**(i+j)*I)
    with dotprodsimp(True):
        assert M.charpoly('x') == PurePoly(x**6 + (-6 - 6*I)*x**5 + 36*I*x**4, x, domain='EX')

