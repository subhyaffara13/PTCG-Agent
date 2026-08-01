
def test_manualintegrate_orthogonal_poly():
    n = symbols('n')
    a, b = 7, Rational(5, 3)
    polys = [jacobi(n, a, b, x), gegenbauer(n, a, x), chebyshevt(n, x),
        chebyshevu(n, x), legendre(n, x), hermite(n, x), laguerre(n, x),
        assoc_laguerre(n, a, x)]
    for p in polys:
        integral = manualintegrate(p, x)
        for deg in [-2, -1, 0, 1, 3, 5, 8]:
            # some accept negative "degree", some do not
            try:
                p_subbed = p.subs(n, deg)
            except ValueError:
                continue
            assert (integral.subs(n, deg).diff(x) - p_subbed).expand() == 0

        # can also integrate simple expressions with these polynomials
        q = x*p.subs(x, 2*x + 1)
        integral = manualintegrate(q, x)
        for deg in [2, 4, 7]:
            assert (integral.subs(n, deg).diff(x) - q.subs(n, deg)).expand() == 0

        # cannot integrate with respect to any other parameter
        t = symbols('t')
        for i in range(len(p.args) - 1):
            new_args = list(p.args)
            new_args[i] = t
            assert isinstance(manualintegrate(p.func(*new_args), t), Integral)

