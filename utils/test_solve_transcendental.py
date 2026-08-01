
def test_solve_transcendental():
    from sympy.abc import a, b

    assert solve(exp(x) - 3, x) == [log(3)]
    assert set(solve((a*x + b)*(exp(x) - 3), x)) == {-b/a, log(3)}
    assert solve(cos(x) - y, x) == [-acos(y) + 2*pi, acos(y)]
    assert solve(2*cos(x) - y, x) == [-acos(y/2) + 2*pi, acos(y/2)]
    assert solve(Eq(cos(x), sin(x)), x) == [pi/4]

    assert set(solve(exp(x) + exp(-x) - y, x)) in [{
        log(y/2 - sqrt(y**2 - 4)/2),
        log(y/2 + sqrt(y**2 - 4)/2),
    }, {
        log(y - sqrt(y**2 - 4)) - log(2),
        log(y + sqrt(y**2 - 4)) - log(2)},
    {
        log(y/2 - sqrt((y - 2)*(y + 2))/2),
        log(y/2 + sqrt((y - 2)*(y + 2))/2)}]
    assert solve(exp(x) - 3, x) == [log(3)]
    assert solve(Eq(exp(x), 3), x) == [log(3)]
    assert solve(log(x) - 3, x) == [exp(3)]
    assert solve(sqrt(3*x) - 4, x) == [Rational(16, 3)]
    assert solve(3**(x + 2), x) == []
    assert solve(3**(2 - x), x) == []
    assert solve(x + 2**x, x) == [-LambertW(log(2))/log(2)]
    assert solve(2*x + 5 + log(3*x - 2), x) == \
        [Rational(2, 3) + LambertW(2*exp(Rational(-19, 3))/3)/2]
    assert solve(3*x + log(4*x), x) == [LambertW(Rational(3, 4))/3]
    assert set(solve((2*x + 8)*(8 + exp(x)), x)) == {S(-4), log(8) + pi*I}
    eq = 2*exp(3*x + 4) - 3
    ans = solve(eq, x)  # this generated a failure in flatten
    assert len(ans) == 3 and all(eq.subs(x, a).n(chop=True) == 0 for a in ans)
    assert solve(2*log(3*x + 4) - 3, x) == [(exp(Rational(3, 2)) - 4)/3]
    assert solve(exp(x) + 1, x) == [pi*I]

    eq = 2*(3*x + 4)**5 - 6*7**(3*x + 9)
    result = solve(eq, x)
    x0 = -log(2401)
    x1 = 3**Rational(1, 5)
    x2 = log(7**(7*x1/20))
    x3 = sqrt(2)
    x4 = sqrt(5)
    x5 = x3*sqrt(x4 - 5)
    x6 = x4 + 1
    x7 = 1/(3*log(7))
    x8 = -x4
    x9 = x3*sqrt(x8 - 5)
    x10 = x8 + 1
    ans = [x7*(x0 - 5*LambertW(x2*(-x5 + x6))),
           x7*(x0 - 5*LambertW(x2*(x5 + x6))),
           x7*(x0 - 5*LambertW(x2*(x10 - x9))),
           x7*(x0 - 5*LambertW(x2*(x10 + x9))),
           x7*(x0 - 5*LambertW(-log(7**(7*x1/5))))]
    assert result == ans, result
    # it works if expanded, too
    assert solve(eq.expand(), x) == result

    assert solve(z*cos(x) - y, x) == [-acos(y/z) + 2*pi, acos(y/z)]
    assert solve(z*cos(2*x) - y, x) == [-acos(y/z)/2 + pi, acos(y/z)/2]
    assert solve(z*cos(sin(x)) - y, x) == [
        pi - asin(acos(y/z)), asin(acos(y/z) - 2*pi) + pi,
        -asin(acos(y/z) - 2*pi), asin(acos(y/z))]

    assert solve(z*cos(x), x) == [pi/2, pi*Rational(3, 2)]

    # issue 4508
    assert solve(y - b*x/(a + x), x) in [[-a*y/(y - b)], [a*y/(b - y)]]
    assert solve(y - b*exp(a/x), x) == [a/log(y/b)]
    # issue 4507
    assert solve(y - b/(1 + a*x), x) in [[(b - y)/(a*y)], [-((y - b)/(a*y))]]
    # issue 4506
    assert solve(y - a*x**b, x) == [(y/a)**(1/b)]
    # issue 4505
    assert solve(z**x - y, x) == [log(y)/log(z)]
    # issue 4504
    assert solve(2**x - 10, x) == [1 + log(5)/log(2)]
    # issue 6744
    assert solve(x*y) == [{x: 0}, {y: 0}]
    assert solve([x*y]) == [{x: 0}, {y: 0}]
    assert solve(x**y - 1) == [{x: 1}, {y: 0}]
    assert solve([x**y - 1]) == [{x: 1}, {y: 0}]
    assert solve(x*y*(x**2 - y**2)) == [{x: 0}, {x: -y}, {x: y}, {y: 0}]
    assert solve([x*y*(x**2 - y**2)]) == [{x: 0}, {x: -y}, {x: y}, {y: 0}]
    # issue 4739
    assert solve(exp(log(5)*x) - 2**x, x) == [0]
    # issue 14791
    assert solve(exp(log(5)*x) - exp(log(2)*x), x) == [0]
    f = Function('f')
    assert solve(y*f(log(5)*x) - y*f(log(2)*x), x) == [0]
    assert solve(f(x) - f(0), x) == [0]
    assert solve(f(x) - f(2 - x), x) == [1]
    raises(NotImplementedError, lambda: solve(f(x, y) - f(1, 2), x))
    raises(NotImplementedError, lambda: solve(f(x, y) - f(2 - x, 2), x))
    raises(ValueError, lambda: solve(f(x, y) - f(1 - x), x))
    raises(ValueError, lambda: solve(f(x, y) - f(1), x))

    # misc
    # make sure that the right variables is picked up in tsolve
    # shouldn't generate a GeneratorsNeeded error in _tsolve when the NaN is generated
    # for eq_down. Actual answers, as determined numerically are approx. +/- 0.83
    raises(NotImplementedError, lambda:
        solve(sinh(x)*sinh(sinh(x)) + cosh(x)*cosh(sinh(x)) - 3))

    # watch out for recursive loop in tsolve
    raises(NotImplementedError, lambda: solve((x + 2)**y*x - 3, x))

    # issue 7245
    assert solve(sin(sqrt(x))) == [0, pi**2]

    # issue 7602
    a, b = symbols('a, b', real=True, negative=False)
    assert str(solve(Eq(a, 0.5 - cos(pi*b)/2), b)) == \
        '[2.0 - 0.318309886183791*acos(1.0 - 2.0*a), 0.318309886183791*acos(1.0 - 2.0*a)]'

    # issue 15325
    assert solve(y**(1/x) - z, x) == [log(y)/log(z)]

    # issue 25685 (basic trig identities should give simple solutions)
    for yi in [cos(2*x),sin(2*x),cos(x - pi/3)]:
        sol = solve([cos(x) - S(3)/5, yi - y])
        assert (sol[0][y] + sol[1][y]).is_Rational, (yi,sol)
    # don't allow massive expansion
    assert solve(cos(1000*x) - S.Half) == [pi/3000, pi/600]
    assert solve(cos(x - 1000*y) - 1, x) == [1000*y, 1000*y + 2*pi]
    assert solve(cos(x + y + z) - 1, x) == [-y - z, -y - z + 2*pi]

    # issue 26008
    assert solve(sin(x + pi/6)) == [-pi/6, 5*pi/6]

