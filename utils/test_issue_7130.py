
def test_issue_7130():
    i, L, a, b = symbols('i L a b')
    integrand = (cos(pi*i*x/L)**2 / (a + b*x)).rewrite(exp)
    assert x not in integrate(integrand, (x, 0, L)).free_symbols

