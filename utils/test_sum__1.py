
def test_sum__1():
    # In each case, test eval() the lambdarepr() to make sure that
    # it evaluates to the same results as the symbolic expression
    s = Sum(x ** i, (i, a, b))
    l = lambdarepr(s)
    assert l == "(builtins.sum(x**i for i in range(a, b+1)))"

    args = x, a, b
    f = lambdify(args, s)
    v = 2, 3, 8
    assert f(*v) == s.subs(zip(args, v)).doit()

