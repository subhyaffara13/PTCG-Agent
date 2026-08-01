
def test_issue_14640():
    i, n = symbols("i n", integer=True)
    a, b, c = symbols("a b c", zero=False)

    assert Sum(a**-i/(a - b), (i, 0, n)).doit() == Sum(
        1/(a*a**i - a**i*b), (i, 0, n)).doit() == Piecewise(
            (n + 1, Eq(1/a, 1)),
            ((-a**(-n - 1) + 1)/(1 - 1/a), True))/(a - b)

    assert Sum((b*a**i - c*a**i)**-2, (i, 0, n)).doit() == Piecewise(
        (n + 1, Eq(a**(-2), 1)),
        ((-a**(-2*n - 2) + 1)/(1 - 1/a**2), True))/(b - c)**2

    s = Sum(i*(a**(n - i) - b**(n - i))/(a - b), (i, 0, n)).doit()
    assert not s.has(Sum)
    assert s.subs({a: 2, b: 3, n: 5}) == 122

