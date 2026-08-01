
def test_PrettyPoly():
    from sympy.polys.domains import QQ
    F = QQ.frac_field(x, y)
    R = QQ[x, y]

    assert latex(F.convert(x/(x + y))) == latex(x/(x + y))
    assert latex(R.convert(x + y)) == latex(x + y)


def test_PrettyPoly():
    F = QQ.frac_field(x, y)
    R = QQ[x, y]
    assert sstr(F.convert(x/(x + y))) == sstr(x/(x + y))
    assert sstr(R.convert(x + y)) == sstr(x + y)


def test_PrettyPoly():
    F = QQ.frac_field(x, y)
    R = QQ.poly_ring(x, y)

    expr = F.convert(x/(x + y))
    assert pretty(expr) == "x/(x + y)"
    assert upretty(expr) == "x/(x + y)"

    expr = R.convert(x + y)
    assert pretty(expr) == "x + y"
    assert upretty(expr) == "x + y"

