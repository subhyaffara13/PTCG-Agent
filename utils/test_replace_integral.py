
def test_replace_integral():
    # https://github.com/sympy/sympy/issues/27142
    q, p, s, t = symbols('q p s t', cls=Wild)
    a, b, c, d = symbols('a b c d')
    i = Integral(a + b, (b, c, d))
    pattern = Integral(q, (p, s, t))
    assert i.replace(pattern, q) == a + b

