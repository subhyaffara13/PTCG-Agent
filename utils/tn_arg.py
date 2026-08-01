
def tn_arg(func):
    def test(arg, e1, e2):
        from sympy.core.random import uniform
        v = uniform(1, 5)
        v1 = func(arg*x).subs(x, v).n()
        v2 = func(e1*v + e2*1e-15).n()
        return abs(v1 - v2).n() < 1e-10
    return test(exp_polar(I*pi/2), I, 1) and \
        test(exp_polar(-I*pi/2), -I, 1) and \
        test(exp_polar(I*pi), -1, I) and \
        test(exp_polar(-I*pi), -1, -I)

