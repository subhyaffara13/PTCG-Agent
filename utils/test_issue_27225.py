
def test_issue_27225():
    # https://github.com/sympy/sympy/issues/27225
    raises(TypeError, lambda : floor(Matrix([1, 1, 0])))

