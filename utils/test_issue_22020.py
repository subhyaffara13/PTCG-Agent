
def test_issue_22020():
    expr = I*pi/2 -oo
    assert simplify(expr) == expr


def test_issue_22020():
    from sympy.parsing.sympy_parser import parse_expr
    x = parse_expr("log((2*V/3-V)/C)/-(R+r)*C")
    y = parse_expr("log((2*V/3-V)/C)/-(R+r)*2")
    assert x.equals(y) is False

