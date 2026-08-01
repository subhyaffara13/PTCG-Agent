
def test_issue_27163():
    # https://github.com/sympy/sympy/issues/27163
    raises(TypeError, lambda: Derivative(f, t))

