
def test_sym_integral():
    f = Lambda(x, exp(-x**2))
    l = lambdify(x, Integral(f(x), (x, -oo, oo)), modules="sympy")
    assert l(y) == Integral(exp(-y**2), (y, -oo, oo))
    assert l(y).doit() == sqrt(pi)

