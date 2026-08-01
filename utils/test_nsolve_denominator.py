
def test_nsolve_denominator():
    x = symbols('x')
    # Test that nsolve uses the full expression (numerator and denominator).
    ans = nsolve((x**2 + 3*x + 2)/(x + 2), -2.1)
    # The root -2 was divided out, so make sure we don't find it.
    assert ans == -1.0

