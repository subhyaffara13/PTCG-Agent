
def _nonlinear_2eq_order1_type1(x, y, t, eq):
    r"""
    Equations:

    .. math:: x' = x^n F(x,y)

    .. math:: y' = g(y) F(x,y)

    Solution:

    .. math:: x = \varphi(y), \int \frac{1}{g(y) F(\varphi(y),y)} \,dy = t + C_2

    where

    if `n \neq 1`

    .. math:: \varphi = [C_1 + (1-n) \int \frac{1}{g(y)} \,dy]^{\frac{1}{1-n}}

    if `n = 1`

    .. math:: \varphi = C_1 e^{\int \frac{1}{g(y)} \,dy}

    where `C_1` and `C_2` are arbitrary constants.

    """
    C1, C2 = get_numbered_constants(eq, num=2)
    n = Wild('n', exclude=[x(t),y(t)])
    f = Wild('f')
    u, v = symbols('u, v')
    r = eq[0].match(diff(x(t),t) - x(t)**n*f)
    g = ((diff(y(t),t) - eq[1])/r[f]).subs(y(t),v)
    F = r[f].subs(x(t),u).subs(y(t),v)
    n = r[n]
    if n!=1:
        phi = (C1 + (1-n)*Integral(1/g, v))**(1/(1-n))
    else:
        phi = C1*exp(Integral(1/g, v))
    phi = phi.doit()
    sol2 = solve(Integral(1/(g*F.subs(u,phi)), v).doit() - t - C2, v)
    sol = []
    for sols in sol2:
        sol.append(Eq(x(t),phi.subs(v, sols)))
        sol.append(Eq(y(t), sols))
    return sol

