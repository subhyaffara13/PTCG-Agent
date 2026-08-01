
def test_issue_17247_expression_blowup_27():
    M = Matrix([
        [    0, 1 - x, x + 1, 1 - x],
        [1 - x, x + 1,     0, x + 1],
        [    0, 1 - x, x + 1, 1 - x],
        [    0,     0,     1 - x, 0]])
    with dotprodsimp(True):
        P, J = M.jordan_form()
        assert P.expand() == Matrix(S('''[
            [    0,  4*x/(x**2 - 2*x + 1), -(-17*x**4 + 12*sqrt(2)*x**4 - 4*sqrt(2)*x**3 + 6*x**3 - 6*x - 4*sqrt(2)*x + 12*sqrt(2) + 17)/(-7*x**4 + 5*sqrt(2)*x**4 - 6*sqrt(2)*x**3 + 8*x**3 - 2*x**2 + 8*x + 6*sqrt(2)*x - 5*sqrt(2) - 7), -(12*sqrt(2)*x**4 + 17*x**4 - 6*x**3 - 4*sqrt(2)*x**3 - 4*sqrt(2)*x + 6*x - 17 + 12*sqrt(2))/(7*x**4 + 5*sqrt(2)*x**4 - 6*sqrt(2)*x**3 - 8*x**3 + 2*x**2 - 8*x + 6*sqrt(2)*x - 5*sqrt(2) + 7)],
            [x - 1, x/(x - 1) + 1/(x - 1),                       (-7*x**3 + 5*sqrt(2)*x**3 - x**2 + sqrt(2)*x**2 - sqrt(2)*x - x - 5*sqrt(2) - 7)/(-3*x**3 + 2*sqrt(2)*x**3 - 2*sqrt(2)*x**2 + 3*x**2 + 2*sqrt(2)*x + 3*x - 3 - 2*sqrt(2)),                       (7*x**3 + 5*sqrt(2)*x**3 + x**2 + sqrt(2)*x**2 - sqrt(2)*x + x - 5*sqrt(2) + 7)/(2*sqrt(2)*x**3 + 3*x**3 - 3*x**2 - 2*sqrt(2)*x**2 - 3*x + 2*sqrt(2)*x - 2*sqrt(2) + 3)],
            [    0,                     1,                                                                                            -(-3*x**2 + 2*sqrt(2)*x**2 + 2*x - 3 - 2*sqrt(2))/(-x**2 + sqrt(2)*x**2 - 2*sqrt(2)*x + 1 + sqrt(2)),                                                                                            -(2*sqrt(2)*x**2 + 3*x**2 - 2*x - 2*sqrt(2) + 3)/(x**2 + sqrt(2)*x**2 - 2*sqrt(2)*x - 1 + sqrt(2))],
            [1 - x,                     0,                                                                                                                                                                                               1,                                                                                                                                                                                             1]]''')).expand()
        assert J == Matrix(S('''[
            [0, 1,                       0,                       0],
            [0, 0,                       0,                       0],
            [0, 0, x - sqrt(2)*(x - 1) + 1,                       0],
            [0, 0,                       0, x + sqrt(2)*(x - 1) + 1]]'''))


def test_issue_17247_expression_blowup_27():
    M = Matrix([
        [    0, 1 - x, x + 1, 1 - x],
        [1 - x, x + 1,     0, x + 1],
        [    0, 1 - x, x + 1, 1 - x],
        [    0,     0,     1 - x, 0]])
    with dotprodsimp(True):
        P, J = M.jordan_form()
        assert P.expand() == Matrix(S('''[
            [    0,  4*x/(x**2 - 2*x + 1), -(-17*x**4 + 12*sqrt(2)*x**4 - 4*sqrt(2)*x**3 + 6*x**3 - 6*x - 4*sqrt(2)*x + 12*sqrt(2) + 17)/(-7*x**4 + 5*sqrt(2)*x**4 - 6*sqrt(2)*x**3 + 8*x**3 - 2*x**2 + 8*x + 6*sqrt(2)*x - 5*sqrt(2) - 7), -(12*sqrt(2)*x**4 + 17*x**4 - 6*x**3 - 4*sqrt(2)*x**3 - 4*sqrt(2)*x + 6*x - 17 + 12*sqrt(2))/(7*x**4 + 5*sqrt(2)*x**4 - 6*sqrt(2)*x**3 - 8*x**3 + 2*x**2 - 8*x + 6*sqrt(2)*x - 5*sqrt(2) + 7)],
            [x - 1, x/(x - 1) + 1/(x - 1),                       (-7*x**3 + 5*sqrt(2)*x**3 - x**2 + sqrt(2)*x**2 - sqrt(2)*x - x - 5*sqrt(2) - 7)/(-3*x**3 + 2*sqrt(2)*x**3 - 2*sqrt(2)*x**2 + 3*x**2 + 2*sqrt(2)*x + 3*x - 3 - 2*sqrt(2)),                       (7*x**3 + 5*sqrt(2)*x**3 + x**2 + sqrt(2)*x**2 - sqrt(2)*x + x - 5*sqrt(2) + 7)/(2*sqrt(2)*x**3 + 3*x**3 - 3*x**2 - 2*sqrt(2)*x**2 - 3*x + 2*sqrt(2)*x - 2*sqrt(2) + 3)],
            [    0,                     1,                                                                                            -(-3*x**2 + 2*sqrt(2)*x**2 + 2*x - 3 - 2*sqrt(2))/(-x**2 + sqrt(2)*x**2 - 2*sqrt(2)*x + 1 + sqrt(2)),                                                                                            -(2*sqrt(2)*x**2 + 3*x**2 - 2*x - 2*sqrt(2) + 3)/(x**2 + sqrt(2)*x**2 - 2*sqrt(2)*x - 1 + sqrt(2))],
            [1 - x,                     0,                                                                                                                                                                                               1,                                                                                                                                                                                             1]]''')).expand()
        assert J == Matrix(S('''[
            [0, 1,                       0,                       0],
            [0, 0,                       0,                       0],
            [0, 0, x - sqrt(2)*(x - 1) + 1,                       0],
            [0, 0,                       0, x + sqrt(2)*(x - 1) + 1]]'''))

