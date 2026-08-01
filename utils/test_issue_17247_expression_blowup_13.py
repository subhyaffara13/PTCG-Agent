
def test_issue_17247_expression_blowup_13():
    M = Matrix([
        [    0, 1 - x, x + 1, 1 - x],
        [1 - x, x + 1,     0, x + 1],
        [    0, 1 - x, x + 1, 1 - x],
        [    0,     0,     1 - x, 0]])

    ev = M.eigenvects()
    assert ev[0] == (0, 2, [Matrix([0, -1, 0, 1])])
    assert ev[1][0] == x - sqrt(2)*(x - 1) + 1
    assert ev[1][1] == 1
    assert ev[1][2][0].expand(deep=False, numer=True) == Matrix([
        [(-x + sqrt(2)*(x - 1) - 1)/(x - 1)],
        [-4*x/(x**2 - 2*x + 1) + (x + 1)*(x - sqrt(2)*(x - 1) + 1)/(x**2 - 2*x + 1)],
        [(-x + sqrt(2)*(x - 1) - 1)/(x - 1)],
        [1]
    ])

    assert ev[2][0] == x + sqrt(2)*(x - 1) + 1
    assert ev[2][1] == 1
    assert ev[2][2][0].expand(deep=False, numer=True) == Matrix([
        [(-x - sqrt(2)*(x - 1) - 1)/(x - 1)],
        [-4*x/(x**2 - 2*x + 1) + (x + 1)*(x + sqrt(2)*(x - 1) + 1)/(x**2 - 2*x + 1)],
        [(-x - sqrt(2)*(x - 1) - 1)/(x - 1)],
        [1]
    ])


def test_issue_17247_expression_blowup_13():
    M = Matrix([
        [    0, 1 - x, x + 1, 1 - x],
        [1 - x, x + 1,     0, x + 1],
        [    0, 1 - x, x + 1, 1 - x],
        [    0,     0,     1 - x, 0]])

    ev = M.eigenvects()
    assert ev[0] == (0, 2, [Matrix([0, -1, 0, 1])])
    assert ev[1][0] == x - sqrt(2)*(x - 1) + 1
    assert ev[1][1] == 1
    assert ev[1][2][0].expand(deep=False, numer=True) == Matrix([
        [(-x + sqrt(2)*(x - 1) - 1)/(x - 1)],
        [-4*x/(x**2 - 2*x + 1) + (x + 1)*(x - sqrt(2)*(x - 1) + 1)/(x**2 - 2*x + 1)],
        [(-x + sqrt(2)*(x - 1) - 1)/(x - 1)],
        [1]
    ])

    assert ev[2][0] == x + sqrt(2)*(x - 1) + 1
    assert ev[2][1] == 1
    assert ev[2][2][0].expand(deep=False, numer=True) == Matrix([
        [(-x - sqrt(2)*(x - 1) - 1)/(x - 1)],
        [-4*x/(x**2 - 2*x + 1) + (x + 1)*(x + sqrt(2)*(x - 1) + 1)/(x**2 - 2*x + 1)],
        [(-x - sqrt(2)*(x - 1) - 1)/(x - 1)],
        [1]
    ])

