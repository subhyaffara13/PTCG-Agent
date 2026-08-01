
def test_issue_7096():
    from sympy.functions import sign
    assert gruntz(x**-pi, x, 0, dir='-') == oo*sign((-1)**(-pi))

