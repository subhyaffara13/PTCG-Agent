
def test_issue_25176():
    eq = (x - 5)**-8 - 3
    sol = solve(eq)
    assert not any(eq.subs(x, i) for i in sol)


def test_issue_25176():
    assert sqrt(-4*3**(S(3)/4)*I/3) == 2*3**(S(7)/8)*sqrt(-I)/3

