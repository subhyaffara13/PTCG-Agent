
def test_expressions():
    assert residue(1/(x + 1), x, 0) == 0
    assert residue(1/(x + 1), x, -1) == 1
    assert residue(1/(x**2 + 1), x, -1) == 0
    assert residue(1/(x**2 + 1), x, I) == -I/2
    assert residue(1/(x**2 + 1), x, -I) == I/2
    assert residue(1/(x**4 + 1), x, 0) == 0
    assert residue(1/(x**4 + 1), x, exp(I*pi/4)).equals(-(Rational(1, 4) + I/4)/sqrt(2))
    assert residue(1/(x**2 + a**2)**2, x, a*I) == -I/4/a**3

