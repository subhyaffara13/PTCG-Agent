
def _inverse_laplace_transform_integration(F, s, t_, plane, *, simplify):
    """ The backend function for inverse Laplace transforms. """
    from sympy.integrals.meijerint import meijerint_inversion, _get_coeff_exp
    from sympy.integrals.transforms import inverse_mellin_transform

    # There are two strategies we can try:
    # 1) Use inverse mellin transform, related by a simple change of variables.
    # 2) Use the inversion integral.

    t = Dummy('t', real=True)

    def pw_simp(*args):
        """ Simplify a piecewise expression from hyperexpand. """
        if len(args) != 3:
            return Piecewise(*args)
        arg = args[2].args[0].argument
        coeff, exponent = _get_coeff_exp(arg, t)
        e1 = args[0].args[0]
        e2 = args[1].args[0]
        return (
            Heaviside(1/Abs(coeff) - t**exponent)*e1 +
            Heaviside(t**exponent - 1/Abs(coeff))*e2)

    if F.is_rational_function(s):
        F = F.apart(s)

    if F.is_Add:
        f = Add(
            *[_inverse_laplace_transform_integration(X, s, t, plane, simplify)
              for X in F.args])
        return _simplify(f.subs(t, t_), simplify), True

    try:
        f, cond = inverse_mellin_transform(F, s, exp(-t), (None, S.Infinity),
                                           needeval=True, noconds=False)
    except IntegralTransformError:
        f = None

    if f is None:
        f = meijerint_inversion(F, s, t)
        if f is None:
            return None
        if f.is_Piecewise:
            f, cond = f.args[0]
            if f.has(Integral):
                return None
        else:
            cond = S.true
        f = f.replace(Piecewise, pw_simp)

    if f.is_Piecewise:
        # many of the functions called below can't work with piecewise
        # (b/c it has a bool in args)
        return f.subs(t, t_), cond

    u = Dummy('u')

    def simp_heaviside(arg, H0=S.Half):
        a = arg.subs(exp(-t), u)
        if a.has(t):
            return Heaviside(arg, H0)
        from sympy.solvers.inequalities import _solve_inequality
        rel = _solve_inequality(a > 0, u)
        if rel.lts == u:
            k = log(rel.gts)
            return Heaviside(t + k, H0)
        else:
            k = log(rel.lts)
            return Heaviside(-(t + k), H0)

    f = f.replace(Heaviside, simp_heaviside)

    def simp_exp(arg):
        return expand_complex(exp(arg))

    f = f.replace(exp, simp_exp)

    return _simplify(f.subs(t, t_), simplify), cond

