
def test_multiple_sums():
    s = Sum(i * x + j, (i, a, b), (j, c, d))

    l = lambdarepr(s)
    assert l == "(builtins.sum(i*x + j for j in range(c, d+1) for i in range(a, b+1)))"

    args = x, a, b, c, d
    f = lambdify(args, s)
    vals = 2, 3, 4, 5, 6
    f_ref = s.subs(zip(args, vals)).doit()
    f_res = f(*vals)
    assert f_res == f_ref


def test_multiple_sums():
    if not np:
        skip("NumPy not installed")

    s = Sum((x + j) * i, (i, a, b), (j, c, d))
    f = lambdify((a, b, c, d, x), s, 'numpy')

    a_, b_ = 0, 10
    c_, d_ = 11, 21
    x_ = np.linspace(-1, +1, 10)
    assert np.allclose(f(a_, b_, c_, d_, x_),
                       sum((x_ + j_) * i_ for i_ in range(a_, b_ + 1) for j_ in range(c_, d_ + 1)))

