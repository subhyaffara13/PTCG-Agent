
def test_issue_22033_integral():
    assert integrate((x**2 - Rational(1, 4))**2 * sqrt(1 - x**2), (x, -1, 1)) == pi/32

