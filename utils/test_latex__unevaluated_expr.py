
def test_latex_UnevaluatedExpr():
    x = symbols("x")
    he = UnevaluatedExpr(1/x)
    assert latex(he) == latex(1/x) == r"\frac{1}{x}"
    assert latex(he**2) == r"\left(\frac{1}{x}\right)^{2}"
    assert latex(he + 1) == r"1 + \frac{1}{x}"
    assert latex(x*he) == r"x \frac{1}{x}"

