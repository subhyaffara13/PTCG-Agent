
def test_issue_4487():
    from sympy.functions.special.gamma_functions import lowergamma
    assert simplify(integrate(exp(-x)*x**y, x)) == lowergamma(y + 1, x)

