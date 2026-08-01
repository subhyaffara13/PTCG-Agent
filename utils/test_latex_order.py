
def test_latex_order():
    expr = x**3 + x**2*y + y**4 + 3*x*y**3

    assert latex(expr, order='lex') == r"x^{3} + x^{2} y + 3 x y^{3} + y^{4}"
    assert latex(
        expr, order='rev-lex') == r"y^{4} + 3 x y^{3} + x^{2} y + x^{3}"
    assert latex(expr, order='none') == r"x^{3} + y^{4} + y x^{2} + 3 x y^{3}"

