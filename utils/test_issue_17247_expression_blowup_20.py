
def test_issue_17247_expression_blowup_20():
    M = Matrix([
    [x + 1,  1 - x,      0,      0],
    [1 - x,  x + 1,      0,  x + 1],
    [    0,  1 - x,  x + 1,      0],
    [    0,      0,      0,  x + 1]])
    with dotprodsimp(True):
        assert M.diagonalize() == (Matrix([
            [1,  1, 0, (x + 1)/(x - 1)],
            [1, -1, 0,               0],
            [1,  1, 1,               0],
            [0,  0, 0,               1]]),
            Matrix([
            [2,   0,     0,     0],
            [0, 2*x,     0,     0],
            [0,   0, x + 1,     0],
            [0,   0,     0, x + 1]]))


def test_issue_17247_expression_blowup_20():
    M = Matrix([
    [x + 1,  1 - x,      0,      0],
    [1 - x,  x + 1,      0,  x + 1],
    [    0,  1 - x,  x + 1,      0],
    [    0,      0,      0,  x + 1]])
    with dotprodsimp(True):
        assert M.diagonalize() == (Matrix([
            [1,  1, 0, (x + 1)/(x - 1)],
            [1, -1, 0,               0],
            [1,  1, 1,               0],
            [0,  0, 0,               1]]),
            Matrix([
            [2,   0,     0,     0],
            [0, 2*x,     0,     0],
            [0,   0, x + 1,     0],
            [0,   0,     0, x + 1]]))

