
def test_apart_full():
    f = 1/(x**2 + 1)

    assert apart(f, full=False) == f
    assert apart(f, full=True).dummy_eq(
        -RootSum(x**2 + 1, Lambda(a, a/(x - a)), auto=False)/2)

    f = 1/(x**3 + x + 1)

    assert apart(f, full=False) == f
    assert apart(f, full=True).dummy_eq(
        RootSum(x**3 + x + 1,
        Lambda(a, (a**2*Rational(6, 31) - a*Rational(9, 31) + Rational(4, 31))/(x - a)), auto=False))

    f = 1/(x**5 + 1)

    assert apart(f, full=False) == \
        (Rational(-1, 5))*((x**3 - 2*x**2 + 3*x - 4)/(x**4 - x**3 + x**2 -
         x + 1)) + (Rational(1, 5))/(x + 1)
    assert apart(f, full=True).dummy_eq(
        -RootSum(x**4 - x**3 + x**2 - x + 1,
        Lambda(a, a/(x - a)), auto=False)/5 + (Rational(1, 5))/(x + 1))

