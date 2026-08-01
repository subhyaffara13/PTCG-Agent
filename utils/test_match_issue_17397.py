
def test_match_issue_17397():
    f = Function("f")
    x = Symbol("x")
    a3 = Wild('a3', exclude=[f(x), f(x).diff(x), f(x).diff(x, 2)])
    b3 = Wild('b3', exclude=[f(x), f(x).diff(x), f(x).diff(x, 2)])
    c3 = Wild('c3', exclude=[f(x), f(x).diff(x), f(x).diff(x, 2)])
    deq = a3*(f(x).diff(x, 2)) + b3*f(x).diff(x) + c3*f(x)

    eq = (x-2)**2*(f(x).diff(x, 2)) + (x-2)*(f(x).diff(x)) + ((x-2)**2 - 4)*f(x)
    r = collect(eq, [f(x).diff(x, 2), f(x).diff(x), f(x)]).match(deq)
    assert r == {a3: (x - 2)**2, c3: (x - 2)**2 - 4, b3: x - 2}

    eq =x*f(x) + x*Derivative(f(x), (x, 2)) - 4*f(x) + Derivative(f(x), x) \
        - 4*Derivative(f(x), (x, 2)) - 2*Derivative(f(x), x)/x + 4*Derivative(f(x), (x, 2))/x
    r = collect(eq, [f(x).diff(x, 2), f(x).diff(x), f(x)]).match(deq)
    assert r == {a3: x - 4 + 4/x, b3: 1 - 2/x, c3: x - 4}

