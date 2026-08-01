
def test_X21():
    """
    Test whether `fourier_series` of x periodical on the [-p, p] interval equals
    `- (2 p / pi) sum( (-1)^n / n sin(n pi x / p), n = 1..infinity )`.
    """
    p = symbols('p', positive=True)
    n = symbols('n', positive=True, integer=True)
    s = fourier_series(x, (x, -p, p))

    # All cosine coefficients are equal to 0
    assert s.an.formula == 0

    # Check for sine coefficients
    assert s.bn.formula.subs(s.bn.variables[0], 0) == 0
    assert s.bn.formula.subs(s.bn.variables[0], n) == \
        -2*p/pi * (-1)**n / n * sin(n*pi*x/p)

