
def test_issue_17247_expression_blowup_32():
    M = Matrix([
        [x + 1, 1 - x,     0,     0],
        [1 - x, x + 1,     0, x + 1],
        [    0, 1 - x, x + 1,     0],
        [    0,     0,     0, x + 1]])
    with dotprodsimp(True):
        assert M.LUsolve(ones(4, 1)) == Matrix([
            [(x + 1)/(4*x)],
            [(x - 1)/(4*x)],
            [(x + 1)/(4*x)],
            [    1/(x + 1)]])

