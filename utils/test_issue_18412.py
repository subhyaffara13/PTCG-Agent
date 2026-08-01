
def test_issue_18412():
    d = (Rational(1, 6) + z / 4 / y)
    assert Eq(x, pi * y**3 * d).replace(y**3, z) == Eq(x, pi * z * d)

