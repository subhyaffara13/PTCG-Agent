
def test_sum__2():
    s = Sum(i * x, (i, a, b))
    l = lambdarepr(s)
    assert l == "(builtins.sum(i*x for i in range(a, b+1)))"

    args = x, a, b
    f = lambdify(args, s)
    v = 2, 3, 8
    assert f(*v) == s.subs(zip(args, v)).doit()

