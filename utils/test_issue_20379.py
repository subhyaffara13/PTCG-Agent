
def test_issue_20379():
    #https://github.com/sympy/sympy/issues/20379
    x = pi - 3.14159265358979
    assert FiniteSet(x).evalf(2) == FiniteSet(Float('3.23108914886517e-15', 2))

