
def test_issue_3664():
    n = Symbol('n', integer=True, nonzero=True)
    assert integrate(-1./2 * x * sin(n * pi * x/2), [x, -2, 0]) == \
        2.0*cos(pi*n)/(pi*n)
    assert integrate(x * sin(n * pi * x/2) * Rational(-1, 2), [x, -2, 0]) == \
        2*cos(pi*n)/(pi*n)

