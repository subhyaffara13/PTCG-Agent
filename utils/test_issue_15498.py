
def test_issue_15498():
    Z0 = Function('Z0')
    k01, k10, t, s= symbols('k01 k10 t s', real=True, positive=True)
    m = Matrix([[exp(-k10*t)]])
    _83 = Rational(83, 100)  # 0.83 works, too
    [a, b, c, d, e, f, g] = [100, 0.5, _83, 50, 0.6, 2, 120]
    AIF_btf = a*(d*e*(1 - exp(-(t - b)/e)) + f*g*(1 - exp(-(t - b)/g)))
    AIF_atf = a*(d*e*exp(-(t - b)/e)*(exp((c - b)/e) - 1
        ) + f*g*exp(-(t - b)/g)*(exp((c - b)/g) - 1))
    AIF_sym = Piecewise((0, t < b), (AIF_btf, And(b <= t, t < c)), (AIF_atf, c <= t))
    aif_eq = Eq(Z0(t), AIF_sym)
    f_vec = Matrix([[k01*Z0(t)]])
    integrand = m*m.subs(t, s)**-1*f_vec.subs(aif_eq.lhs, aif_eq.rhs).subs(t, s)
    solution = integrate(integrand[0], (s, 0, t))
    assert solution is not None  # does not hang and takes less than 10 s

