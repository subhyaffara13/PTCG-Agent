
def _nonlinear_2eq_order1_type3(x, y, t, eq):
    r"""
    Autonomous system of general form

    .. math:: x' = F(x,y)

    .. math:: y' = G(x,y)

    Assuming `y = y(x, C_1)` where `C_1` is an arbitrary constant is the general
    solution of the first-order equation

    .. math:: F(x,y) y'_x = G(x,y)

    Then the general solution of the original system of equations has the form

    .. math:: \int \frac{1}{F(x,y(x,C_1))} \,dx = t + C_1

    """
    C1, C2, C3, C4 = get_numbered_constants(eq, num=4)
    v = Function('v')
    u = Symbol('u')
    f = Wild('f')
    g = Wild('g')
    r1 = eq[0].match(diff(x(t),t) - f)
    r2 = eq[1].match(diff(y(t),t) - g)
    F = r1[f].subs(x(t), u).subs(y(t), v(u))
    G = r2[g].subs(x(t), u).subs(y(t), v(u))
    sol2r = dsolve(Eq(diff(v(u), u), G/F))
    if isinstance(sol2r, Equality):
        sol2r = [sol2r]
    for sol2s in sol2r:
        sol1 = solve(Integral(1/F.subs(v(u), sol2s.rhs), u).doit() - t - C2, u)
    sol = []
    for sols in sol1:
        sol.append(Eq(x(t), sols))
        sol.append(Eq(y(t), (sol2s.rhs).subs(u, sols)))
    return sol

