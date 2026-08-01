
def test_issue_11726():
    x, t = symbols("x t")
    f  = symbols("f", cls=Function)
    X, T = symbols("X T", cls=Function)

    u = f(x, t)
    eq = u.diff(x, 2) - u.diff(t, 2)
    res = pde_separate(eq, u, [T(x), X(t)])
    assert res == [D(T(x), x, x)/T(x),D(X(t), t, t)/X(t)]

