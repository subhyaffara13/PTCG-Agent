
def test_issue_17247_expression_blowup_14():
    M = Matrix(8, 8, ([1+x, 1-x]*4 + [1-x, 1+x]*4)*4)
    with dotprodsimp(True):
        assert M.echelon_form() == Matrix([
            [x + 1, 1 - x, x + 1, 1 - x, x + 1, 1 - x, x + 1, 1 - x],
            [    0,   4*x,     0,   4*x,     0,   4*x,     0,   4*x],
            [    0,     0,     0,     0,     0,     0,     0,     0],
            [    0,     0,     0,     0,     0,     0,     0,     0],
            [    0,     0,     0,     0,     0,     0,     0,     0],
            [    0,     0,     0,     0,     0,     0,     0,     0],
            [    0,     0,     0,     0,     0,     0,     0,     0],
            [    0,     0,     0,     0,     0,     0,     0,     0]])


def test_issue_17247_expression_blowup_14():
    M = Matrix(8, 8, ([1+x, 1-x]*4 + [1-x, 1+x]*4)*4)
    with dotprodsimp(True):
        assert M.echelon_form() == Matrix([
            [x + 1, 1 - x, x + 1, 1 - x, x + 1, 1 - x, x + 1, 1 - x],
            [    0,   4*x,     0,   4*x,     0,   4*x,     0,   4*x],
            [    0,     0,     0,     0,     0,     0,     0,     0],
            [    0,     0,     0,     0,     0,     0,     0,     0],
            [    0,     0,     0,     0,     0,     0,     0,     0],
            [    0,     0,     0,     0,     0,     0,     0,     0],
            [    0,     0,     0,     0,     0,     0,     0,     0],
            [    0,     0,     0,     0,     0,     0,     0,     0]])

