
def tn_branch(func, s=None):
    from sympy.core.random import uniform

    def fn(x):
        if s is None:
            return func(x)
        return func(s, x)
    c = uniform(1, 5)
    expr = fn(c*exp_polar(I*pi)) - fn(c*exp_polar(-I*pi))
    eps = 1e-15
    expr2 = fn(-c + eps*I) - fn(-c - eps*I)
    return abs(expr.n() - expr2.n()).n() < 1e-10


def tn_branch(s, func):
    from sympy.core.random import uniform
    c = uniform(1, 5)
    expr = func(s, c*exp_polar(I*pi)) - func(s, c*exp_polar(-I*pi))
    eps = 1e-15
    expr2 = func(s + eps, -c + eps*I) - func(s + eps, -c - eps*I)
    return abs(expr.n() - expr2.n()).n() < 1e-10

