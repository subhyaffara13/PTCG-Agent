
def test_P9():
    a, b, c = symbols('a b c', nonzero=True)
    M = Matrix([[a/(b*c), 1/c, 1/b],
                [1/c, b/(a*c), 1/a],
                [1/b, 1/a, c/(a*b)]])
    assert factor(M.norm('fro')) == (a**2 + b**2 + c**2)/(abs(a)*abs(b)*abs(c))

