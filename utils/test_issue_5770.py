
def test_issue_5770():
    k = Symbol("k", real=True)
    t = Symbol('t')
    w = Function('w')
    sol = dsolve(w(t).diff(t, 6) - k**6*w(t), w(t))
    assert len([s for s in sol.free_symbols if s.name.startswith('C')]) == 6
    assert constantsimp((C1*cos(x) + C2*cos(x))*exp(x), {C1, C2}) == \
        C1*cos(x)*exp(x)
    assert constantsimp(C1*cos(x) + C2*cos(x) + C3*sin(x), {C1, C2, C3}) == \
        C1*cos(x) + C3*sin(x)
    assert constantsimp(exp(C1 + x), {C1}) == C1*exp(x)
    assert constantsimp(x + C1 + y, {C1, y}) == C1 + x
    assert constantsimp(x + C1 + Integral(x, (x, 1, 2)), {C1}) == C1 + x

