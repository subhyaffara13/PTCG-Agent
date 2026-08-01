
def test_issue_17247_expression_blowup_2():
    M = Matrix([[1+x, 1-x], [1-x, 1+x]])
    with dotprodsimp(True):
        P, J = M.jordan_form ()
        assert P*J*P.inv()


def test_issue_17247_expression_blowup_2():
    M = Matrix([[1+x, 1-x], [1-x, 1+x]])
    with dotprodsimp(True):
        P, J = M.jordan_form ()
        assert P*J*P.inv()

