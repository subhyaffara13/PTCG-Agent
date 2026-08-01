
def test_roots_binomial():
    assert roots_binomial(Poly(5*x, x)) == [0]
    assert roots_binomial(Poly(5*x**4, x)) == [0, 0, 0, 0]
    assert roots_binomial(Poly(5*x + 2, x)) == [Rational(-2, 5)]

    A = 10**Rational(3, 4)/10

    assert roots_binomial(Poly(5*x**4 + 2, x)) == \
        [-A - A*I, -A + A*I, A - A*I, A + A*I]
    _check(roots_binomial(Poly(x**8 - 2)))

    a1 = Symbol('a1', nonnegative=True)
    b1 = Symbol('b1', nonnegative=True)

    r0 = roots_quadratic(Poly(a1*x**2 + b1, x))
    r1 = roots_binomial(Poly(a1*x**2 + b1, x))

    assert powsimp(r0[0]) == powsimp(r1[0])
    assert powsimp(r0[1]) == powsimp(r1[1])
    for a, b, s, n in product((1, 2), (1, 2), (-1, 1), (2, 3, 4, 5)):
        if a == b and a != 1:  # a == b == 1 is sufficient
            continue
        p = Poly(a*x**n + s*b)
        ans = roots_binomial(p)
        assert ans == _nsort(ans)

    # issue 8813
    assert roots(Poly(2*x**3 - 16*y**3, x)) == {
        2*y*(Rational(-1, 2) - sqrt(3)*I/2): 1,
        2*y: 1,
        2*y*(Rational(-1, 2) + sqrt(3)*I/2): 1}

