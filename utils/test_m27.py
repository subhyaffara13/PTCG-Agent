
def test_M27():
    x = symbols('x', real=True)
    b = symbols('b', real=True)
    # TODO: Replace solve with solveset which gives both [+/- current answer]
    # note that there is a typo in this test in the wester.pdf; there is no
    # real solution for the equation as it appears in wester.pdf
    assert solve(log(acos(asin(x**R(2, 3) - b)) - 1) + 2, x
        ) == [(b + sin(cos(exp(-2) + 1)))**R(3, 2)]

