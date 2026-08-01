
def test_issue_5132():
    r, t = symbols('r,t')
    assert set(solve([r - x**2 - y**2, tan(t) - y/x], [x, y])) == \
        {(
            -sqrt(r*cos(t)**2), -1*sqrt(r*cos(t)**2)*tan(t)),
            (sqrt(r*cos(t)**2), sqrt(r*cos(t)**2)*tan(t))}
    assert solve([exp(x) - sin(y), 1/y - 3], [x, y]) == \
        [(log(sin(Rational(1, 3))), Rational(1, 3))]
    assert solve([exp(x) - sin(y), 1/exp(y) - 3], [x, y]) == \
        [(log(-sin(log(3))), -log(3))]
    assert set(solve([exp(x) - sin(y), y**2 - 4], [x, y])) == \
        {(log(-sin(2)), -S(2)), (log(sin(2)), S(2))}
    eqs = [exp(x)**2 - sin(y) + z**2, 1/exp(y) - 3]
    assert solve(eqs, set=True) == \
        ([y, z], {
        (-log(3), sqrt(-exp(2*x) - sin(log(3)))),
        (-log(3), -sqrt(-exp(2*x) - sin(log(3))))})
    assert solve(eqs, x, z, set=True) == (
        [x, z],
        {(x, sqrt(-exp(2*x) + sin(y))), (x, -sqrt(-exp(2*x) + sin(y)))})
    assert set(solve(eqs, x, y)) == \
        {
            (log(-sqrt(-z**2 - sin(log(3)))), -log(3)),
        (log(-z**2 - sin(log(3)))/2, -log(3))}
    assert set(solve(eqs, y, z)) == \
        {
            (-log(3), -sqrt(-exp(2*x) - sin(log(3)))),
        (-log(3), sqrt(-exp(2*x) - sin(log(3))))}
    eqs = [exp(x)**2 - sin(y) + z, 1/exp(y) - 3]
    assert solve(eqs, set=True) == ([y, z], {
        (-log(3), -exp(2*x) - sin(log(3)))})
    assert solve(eqs, x, z, set=True) == (
        [x, z], {(x, -exp(2*x) + sin(y))})
    assert set(solve(eqs, x, y)) == {
            (log(-sqrt(-z - sin(log(3)))), -log(3)),
            (log(-z - sin(log(3)))/2, -log(3))}
    assert solve(eqs, z, y) == \
        [(-exp(2*x) - sin(log(3)), -log(3))]
    assert solve((sqrt(x**2 + y**2) - sqrt(10), x + y - 4), set=True) == (
        [x, y], {(S.One, S(3)), (S(3), S.One)})
    assert set(solve((sqrt(x**2 + y**2) - sqrt(10), x + y - 4), x, y)) == \
        {(S.One, S(3)), (S(3), S.One)}

