
def test_inverse_laplace_transform_old():
    from sympy.functions.special.delta_functions import DiracDelta
    ILT = inverse_laplace_transform
    a, b, c, d = symbols('a b c d', positive=True)
    n, r = symbols('n, r', real=True)
    t, z = symbols('t z')
    f = Function('f')
    F = Function('F')

    def simp_hyp(expr):
        return factor_terms(expand_mul(expr)).rewrite(sin)

    L = ILT(F(s), s, t)
    assert laplace_correspondence(L, {f: F}) == f(t)
    assert ILT(exp(-a*s)/s, s, t) == Heaviside(-a + t)
    assert ILT(exp(-a*s)/(b + s), s, t) == exp(-b*(-a + t))*Heaviside(-a + t)
    assert (ILT((b + s)/(a**2 + (b + s)**2), s, t) ==
            exp(-b*t)*cos(a*t)*Heaviside(t))
    assert (ILT(exp(-a*s)/s**b, s, t) ==
            (-a + t)**(b - 1)*Heaviside(-a + t)/gamma(b))
    assert (ILT(exp(-a*s)/sqrt(s**2 + 1), s, t) ==
            Heaviside(-a + t)*besselj(0, a - t))
    assert ILT(1/(s*sqrt(s + 1)), s, t) == Heaviside(t)*erf(sqrt(t))
    # TODO sinh/cosh shifted come out a mess. also delayed trig is a mess
    # TODO should this simplify further?
    assert (ILT(exp(-a*s)/s**b, s, t) ==
            (t - a)**(b - 1)*Heaviside(t - a)/gamma(b))
    assert (ILT(exp(-a*s)/sqrt(1 + s**2), s, t) ==
            Heaviside(t - a)*besselj(0, a - t))  # note: besselj(0, x) is even
    # XXX ILT turns these branch factor into trig functions ...
    assert (
        simplify(ILT(a**b*(s + sqrt(s**2 - a**2))**(-b)/sqrt(s**2 - a**2),
                     s, t).rewrite(exp)) ==
        Heaviside(t)*besseli(b, a*t))
    assert (
        ILT(a**b*(s + sqrt(s**2 + a**2))**(-b)/sqrt(s**2 + a**2),
            s, t, simplify=True).rewrite(exp) ==
        Heaviside(t)*besselj(b, a*t))
    assert ILT(1/(s*sqrt(s + 1)), s, t) == Heaviside(t)*erf(sqrt(t))
    # TODO can we make erf(t) work?
    assert (ILT((s * eye(2) - Matrix([[1, 0], [0, 2]])).inv(), s, t) ==
            Matrix([[exp(t)*Heaviside(t), 0], [0, exp(2*t)*Heaviside(t)]]))
    # Test time_diff rule
    assert (ILT(s**42*f(s), s, t) ==
            Derivative(InverseLaplaceTransform(f(s), s, t, None), (t, 42)))
    assert ILT(cos(s), s, t) == InverseLaplaceTransform(cos(s), s, t, None)
    # Rules for testing different DiracDelta cases
    assert (
        ILT(1 + 2*s + 3*s**2 + 5*s**3, s, t) == DiracDelta(t) +
        2*DiracDelta(t, 1) + 3*DiracDelta(t, 2) + 5*DiracDelta(t, 3))
    assert (ILT(2*exp(3*s) - 5*exp(-7*s), s, t) ==
            2*InverseLaplaceTransform(exp(3*s), s, t, None) -
            5*DiracDelta(t - 7))
    a = cos(sin(7)/2)
    assert ILT(a*exp(-3*s), s, t) == a*DiracDelta(t - 3)
    assert ILT(exp(2*s), s, t) == InverseLaplaceTransform(exp(2*s), s, t, None)
    r = Symbol('r', real=True)
    assert ILT(exp(r*s), s, t) == InverseLaplaceTransform(exp(r*s), s, t, None)
    # Rules for testing whether Heaviside(t) is treated properly in diff rule
    assert ILT(s**2/(a**2 + s**2), s, t) == (
        -a*sin(a*t)*Heaviside(t) + DiracDelta(t))
    assert ILT(s**2*(f(s) + 1/(a**2 + s**2)), s, t) == (
        -a*sin(a*t)*Heaviside(t) + DiracDelta(t) +
        Derivative(InverseLaplaceTransform(f(s), s, t, None), (t, 2)))
    # Rules from the previous test_inverse_laplace_transform_delta_cond():
    assert (ILT(exp(r*s), s, t, noconds=False) ==
            (InverseLaplaceTransform(exp(r*s), s, t, None), True))
    # inversion does not exist: verify it doesn't evaluate to DiracDelta
    for z in (Symbol('z', extended_real=False),
              Symbol('z', imaginary=True, zero=False)):
        f = ILT(exp(z*s), s, t, noconds=False)
        f = f[0] if isinstance(f, tuple) else f
        assert f.func != DiracDelta

