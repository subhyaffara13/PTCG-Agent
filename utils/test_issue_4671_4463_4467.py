
def test_issue_4671_4463_4467():
    assert solve(sqrt(x**2 - 1) - 2) in ([sqrt(5), -sqrt(5)],
                                           [-sqrt(5), sqrt(5)])
    assert solve((2**exp(y**2/x) + 2)/(x**2 + 15), y) == [
        -sqrt(x*log(1 + I*pi/log(2))), sqrt(x*log(1 + I*pi/log(2)))]

    C1, C2 = symbols('C1 C2')
    f = Function('f')
    assert solve(C1 + C2/x**2 - exp(-f(x)), f(x)) == [log(x**2/(C1*x**2 + C2))]
    a = Symbol('a')
    E = S.Exp1
    assert solve(1 - log(a + 4*x**2), x) in (
        [-sqrt(-a + E)/2, sqrt(-a + E)/2],
        [sqrt(-a + E)/2, -sqrt(-a + E)/2]
    )
    assert solve(log(a**(-3) - x**2)/a, x) in (
        [-sqrt(-1 + a**(-3)), sqrt(-1 + a**(-3))],
        [sqrt(-1 + a**(-3)), -sqrt(-1 + a**(-3))],)
    assert solve(1 - log(a + 4*x**2), x) in (
        [-sqrt(-a + E)/2, sqrt(-a + E)/2],
        [sqrt(-a + E)/2, -sqrt(-a + E)/2],)
    assert solve((a**2 + 1)*(sin(a*x) + cos(a*x)), x) == [-pi/(4*a)]
    assert solve(3 - (sinh(a*x) + cosh(a*x)), x) == [log(3)/a]
    assert set(solve(3 - (sinh(a*x) + cosh(a*x)**2), x)) == \
        {log(-2 + sqrt(5))/a, log(-sqrt(2) + 1)/a,
        log(-sqrt(5) - 2)/a, log(1 + sqrt(2))/a}
    assert solve(atan(x) - 1) == [tan(1)]

