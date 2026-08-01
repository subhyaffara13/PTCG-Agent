
def test_issue_6644():
    eq = -sqrt((m - q)**2 + (-m/(2*q) + S.Half)**2) + sqrt((-m**2/2 - sqrt(
    4*m**4 - 4*m**2 + 8*m + 1)/4 - Rational(1, 4))**2 + (m**2/2 - m - sqrt(
    4*m**4 - 4*m**2 + 8*m + 1)/4 - Rational(1, 4))**2)
    sol = solve(eq, q, simplify=False, check=False)
    assert len(sol) == 5

