
def test_PR1964():
    # issue 5171
    assert solve(sqrt(x)) == solve(sqrt(x**3)) == [0]
    assert solve(sqrt(x - 1)) == [1]
    # issue 4462
    a = Symbol('a')
    assert solve(-3*a/sqrt(x), x) == []
    # issue 4486
    assert solve(2*x/(x + 2) - 1, x) == [2]
    # issue 4496
    assert set(solve((x**2/(7 - x)).diff(x))) == {S.Zero, S(14)}
    # issue 4695
    f = Function('f')
    assert solve((3 - 5*x/f(x))*f(x), f(x)) == [x*Rational(5, 3)]
    # issue 4497
    assert solve(1/root(5 + x, 5) - 9, x) == [Rational(-295244, 59049)]

    assert solve(sqrt(x) + sqrt(sqrt(x)) - 4) == [(Rational(-1, 2) + sqrt(17)/2)**4]
    assert set(solve(Poly(sqrt(exp(x)) + sqrt(exp(-x)) - 4))) in \
        [
            {log((-sqrt(3) + 2)**2), log((sqrt(3) + 2)**2)},
            {2*log(-sqrt(3) + 2), 2*log(sqrt(3) + 2)},
            {log(-4*sqrt(3) + 7), log(4*sqrt(3) + 7)},
        ]
    assert set(solve(Poly(exp(x) + exp(-x) - 4))) == \
        {log(-sqrt(3) + 2), log(sqrt(3) + 2)}
    assert set(solve(x**y + x**(2*y) - 1, x)) == \
        {(Rational(-1, 2) + sqrt(5)/2)**(1/y), (Rational(-1, 2) - sqrt(5)/2)**(1/y)}

    assert solve(exp(x/y)*exp(-z/y) - 2, y) == [(x - z)/log(2)]
    assert solve(
        x**z*y**z - 2, z) in [[log(2)/(log(x) + log(y))], [log(2)/(log(x*y))]]
    # if you do inversion too soon then multiple roots (as for the following)
    # will be missed, e.g. if exp(3*x) = exp(3) -> 3*x = 3
    E = S.Exp1
    assert solve(exp(3*x) - exp(3), x) in [
        [1, log(E*(Rational(-1, 2) - sqrt(3)*I/2)), log(E*(Rational(-1, 2) + sqrt(3)*I/2))],
        [1, log(-E/2 - sqrt(3)*E*I/2), log(-E/2 + sqrt(3)*E*I/2)],
        ]

    # coverage test
    p = Symbol('p', positive=True)
    assert solve((1/p + 1)**(p + 1)) == []

