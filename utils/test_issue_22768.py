
def test_issue_22768():
    eq = 2*x**3 - 16*(y - 1)**6*z**3
    assert solve(eq.expand(), x, simplify=False
        ) == [2*z*(y - 1)**2, z*(-1 + sqrt(3)*I)*(y - 1)**2,
        -z*(1 + sqrt(3)*I)*(y - 1)**2]


def test_issue_22768():
    e = Rational(1, 3)
    r = (-1/a)**e*(a + 1)**(5*e)
    assert roots(Poly(a*x**3 + (a + 1)**5, x)) == {
        r: 1,
        -r*(1 + sqrt(3)*I)/2: 1,
        r*(-1 + sqrt(3)*I)/2: 1}

