
def test_other_sums():
    f = m**2 + m*exp(m)
    g = 3*exp(Rational(3, 2))/2 + exp(S.Half)/2 - exp(Rational(-1, 2))/2 - 3*exp(Rational(-3, 2))/2 + 5

    assert summation(f, (m, Rational(-3, 2), Rational(3, 2))) == g
    assert summation(f, (m, -1.5, 1.5)).evalf().epsilon_eq(g.evalf(), 1e-10)

